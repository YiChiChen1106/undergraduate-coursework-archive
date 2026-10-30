import os
import logging
from PIL import Image
import torch
import torch.utils.data as data
from pycocotools.coco import COCO
from torchvision import transforms
from collections import defaultdict
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True  # Handle truncated image files

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MyCOCODataset(data.Dataset):
    def __init__(self, data_root, annofile, output_size=(224, 224), is_train=True, transform=None):
        """
        Initialize COCO dataset
        Args:
            data_root (str): Image root directory
            annofile (str): Annotation file path
            output_size (tuple): Output image size
            is_train (bool): Whether in training mode
            transform (torchvision.transforms.Compose, optional): Custom transforms
        """
        self.data_root = data_root
        self.annofile = annofile
        self.is_train = is_train
        self.output_size = output_size
        self.image_cache = {}  # Add image cache

        # Check paths
        if not os.path.exists(data_root):
            raise FileNotFoundError(f"Data root not found: {data_root}")
        if not os.path.exists(annofile):
            raise FileNotFoundError(f"Annotation file not found: {annofile}")

        # Initialize COCO
        self.coco = COCO(annofile)
        self.all_ann_ids = list(self.coco.anns.keys())
        self.all_anns = self.coco.anns

        # Get all categories and create mappings
        self.category_ids = sorted(self.coco.getCatIds())
        self.num_classes = len(self.category_ids)
        self.catid_to_idx = {cat_id: idx for idx, cat_id in enumerate(self.category_ids)}
        self.idx_to_catid = {idx: cat_id for cat_id, idx in self.catid_to_idx.items()}
        self.categories = [self.coco.cats[cat_id]['name'] for cat_id in self.category_ids]

        logger.info(f"Number of categories: {self.num_classes}")
        logger.info(f"Categories: {self.categories}")

        # Cache image paths
        self.img_id_to_path = {}
        for img in self.coco.loadImgs(self.coco.getImgIds()):
            img_path = os.path.join(self.data_root, img['file_name'])
            self.img_id_to_path[img['id']] = img_path

        # Pre-filter invalid samples and calculate class distribution
        self._filter_samples()

        # Count samples for each class
        self._print_class_distribution()

        # Calculate class weights
        self.class_weights = self._calculate_class_weights()
        logger.info(f"Class weights: {self.class_weights}")

        # Set data augmentation
        self.transform = transform if transform else self._get_default_transforms()

    def _get_default_transforms(self):
        """Get default data augmentation strategy"""
        if self.is_train:
            return transforms.Compose([
                # Basic adjustments
                transforms.Resize((int(self.output_size[0]*1.2), int(self.output_size[1]*1.2))),
                transforms.RandomResizedCrop(
                    self.output_size, 
                    scale=(0.7, 1.0),
                    ratio=(0.75, 1.333)
                ),
                
                # Geometric transformations
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomVerticalFlip(p=0.2),
                transforms.RandomRotation(15),
                transforms.RandomAffine(
                    degrees=10, 
                    translate=(0.1, 0.1),
                    scale=(0.9, 1.1)
                ),
                
                # Color transformations
                transforms.ColorJitter(
                    brightness=0.3,
                    contrast=0.3,
                    saturation=0.3,
                    hue=0.1
                ),
                transforms.RandomAutocontrast(p=0.2),
                transforms.RandomEqualize(p=0.2),
                
                # Blur and noise
                transforms.RandomApply([
                    transforms.GaussianBlur(kernel_size=3)
                ], p=0.1),
                
                # Normalization
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                ),
                transforms.RandomErasing(p=0.2)
            ])
        else:
            return transforms.Compose([
                transforms.Resize(self.output_size),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])

    def _filter_samples(self):
        """Filter invalid samples and calculate class distribution"""
        self.valid_instance_ids = []
        self.class_counts = defaultdict(int)

        logger.info("Starting to filter invalid samples...")
        total_samples = len(self.all_ann_ids)
        valid_count = 0

        for ann_id in self.all_ann_ids:
            ann = self.all_anns[ann_id]
            img_id = ann["image_id"]
            category_id = ann["category_id"]
            mapped_label = self.catid_to_idx.get(category_id, None)

            if mapped_label is None:
                continue

            img_path = self.img_id_to_path.get(img_id, None)
            if img_path is None or not os.path.exists(img_path):
                continue

            try:
                img = Image.open(img_path)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                if min(img.size) < 32:  # Minimum size threshold
                    continue
                
                # Check bbox validity
                bbox = ann.get("bbox", [])
                if len(bbox) != 4 or not all(isinstance(x, (int, float)) for x in bbox):
                    continue
                
                self.valid_instance_ids.append(ann_id)
                self.class_counts[mapped_label] += 1
                valid_count += 1
                
                # Print progress periodically
                if valid_count % 1000 == 0:
                    logger.info(f"Processed {valid_count}/{total_samples} samples...")
                
            except Exception as e:
                continue

        logger.info(f"Filtering completed. Valid instances: {len(self.valid_instance_ids)}")

    def _print_class_distribution(self):
        """Print sample distribution for each class"""
        total_samples = sum(self.class_counts.values())
        logger.info("\n=== Class Distribution ===")
        for idx, count in self.class_counts.items():
            category_name = self.categories[idx]
            percentage = (count / total_samples) * 100 if total_samples > 0 else 0
            logger.info(f"{category_name:15s}: {count:5d} samples ({percentage:5.1f}%)")
        logger.info("==========================\n")

    def _calculate_class_weights(self):
        """Calculate class weights to handle class imbalance"""
        total_samples = sum(self.class_counts.values())
        if total_samples == 0:
            logger.warning("Total samples is zero. Using uniform weights.")
            return torch.ones(self.num_classes)

        weights = []
        # Use frequency-based weight calculation
        frequencies = np.array([self.class_counts.get(i, 0) for i in range(self.num_classes)])
        frequencies = np.where(frequencies > 0, frequencies, 1)  # Avoid division by zero
        weights = np.median(frequencies) / frequencies
        weights = np.clip(weights, 0.1, 10.0)  # Limit weight range

        return torch.tensor(weights, dtype=torch.float)

    def _validate_and_load_image(self, img_path):
        """Validate and load image, using cache"""
        if img_path in self.image_cache:
            return self.image_cache[img_path].copy()

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not found: {img_path}")

        try:
            img = Image.open(img_path)
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Validate image size
            if min(img.size) < 32:
                raise ValueError(f"Image too small: {img.size}")

            # Cache image (limit cache size)
            if len(self.image_cache) < 1000:  # Cache maximum 1000 images
                self.image_cache[img_path] = img.copy()

            return img
        except Exception as e:
            logger.error(f"Error loading image {img_path}: {str(e)}")
            raise

    def _process_bbox(self, bbox, img_size):
        """Process and validate bounding box"""
        x, y, w, h = bbox

        # Ensure bbox is within image bounds
        x = max(0, min(x, img_size[0]-1))
        y = max(0, min(y, img_size[1]-1))
        w = min(w, img_size[0]-x)
        h = min(h, img_size[1]-y)

        # Handle invalid bbox
        if w < 10 or h < 10:
            # Return bbox for entire image
            return [0, 0, img_size[0], img_size[1]]

        # Add bbox context
        context = 0.2
        dx = int(w * context)
        dy = int(h * context)
        
        x = max(0, x - dx)
        y = max(0, y - dy)
        w = min(img_size[0] - x, w + 2*dx)
        h = min(img_size[1] - y, h + 2*dy)

        return [x, y, w, h]

    def _crop_and_process_image(self, img, bbox):
        """Crop and process image"""
        try:
            # Process bbox
            bbox = self._process_bbox(bbox, img.size)
            x, y, w, h = map(int, bbox)

            # Crop image
            cropped = img.crop((x, y, x+w, y+h))

            # Validate crop result
            if min(cropped.size) < 32:
                return img

            return cropped
        except Exception as e:
            logger.warning(f"Error in crop_and_process_image: {str(e)}")
            return img

    def __getitem__(self, index):
        """Get one sample from dataset"""
        ann_id = self.valid_instance_ids[index]
        ann = self.all_anns[ann_id]
        img_id = ann["image_id"]
        bbox = ann["bbox"]
        category_id = ann["category_id"]
        mapped_label = self.catid_to_idx[category_id]

        # Load and process image
        img_path = self.img_id_to_path[img_id]
        img = self._validate_and_load_image(img_path)
        processed_img = self._crop_and_process_image(img, bbox)

        # Apply data augmentation
        if self.transform:
            transformed_img = self.transform(processed_img)
        else:
            transformed_img = transforms.ToTensor()(processed_img)

        # Get class weight
        weight = self.class_weights[mapped_label]

        return transformed_img, torch.tensor(mapped_label, dtype=torch.long), weight

    def __len__(self):
        """Return dataset size"""
        return len(self.valid_instance_ids)

    def get_class_names(self):
        """Get all class names"""
        return {idx: name for idx, name in enumerate(self.categories)}

    def get_dataset_stats(self):
        """Get dataset statistics"""
        stats = {
            'num_classes': self.num_classes,
            'class_distribution': dict(self.class_counts),
            'total_samples': len(self.valid_instance_ids),
            'class_weights': self.class_weights.tolist(),
            'categories': self.categories
        }
        return stats

if __name__ == "__main__":
    # Test dataset
    try:
        data_root = "C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/coco"
        annofile = "C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/coco/annotations.json"

        # Create dataset
        dataset = MyCOCODataset(
            data_root=data_root,
            annofile=annofile,
            is_train=True
        )

        # Test data loading
        logger.info("\nTesting data loading...")
        for i in range(min(5, len(dataset))):
            try:
                img, label, weight = dataset[i]
                logger.info(f"\nSample {i}:")
                logger.info(f"Image shape: {img.shape}")
                logger.info(f"Label: {label.item()}")
                logger.info(f"Weight: {weight.item()}")
                class_names = dataset.get_class_names()
                logger.info(f"Category name: {class_names.get(label.item(), 'Unknown')}")
            except Exception as e:
                logger.error(f"Error loading sample {i}: {str(e)}")

        # Print dataset statistics
        stats = dataset.get_dataset_stats()
        logger.info("\nDataset Statistics:")
        logger.info(f"Total samples: {stats['total_samples']}")
        logger.info(f"Number of classes: {stats['num_classes']}")
        logger.info("Class distribution:")
        for idx, count in stats['class_distribution'].items():
            category = stats['categories'][idx]
            logger.info(f"{category:15s}: {count:5d} samples")
            
        # Test data augmentation consistency
        logger.info("\nTesting data augmentation consistency...")
        test_sample, _, _ = dataset[0]
        augmented_samples = []
        for _ in range(3):
            aug_sample, _, _ = dataset[0]
            augmented_samples.append(aug_sample)
        
        # Check differences between augmented images (verify randomness)
        differences = [torch.abs(augmented_samples[i] - augmented_samples[i-1]).mean().item() 
                      for i in range(1, len(augmented_samples))]
        logger.info(f"Average difference between augmented samples: {np.mean(differences):.4f}")
        
        # Test bbox processing
        logger.info("\nTesting bbox processing...")
        ann_id = dataset.valid_instance_ids[0]
        ann = dataset.all_anns[ann_id]
        img_id = ann["image_id"]
        img_path = dataset.img_id_to_path[img_id]
        original_bbox = ann["bbox"]
        img = dataset._validate_and_load_image(img_path)
        processed_bbox = dataset._process_bbox(original_bbox, img.size)
        logger.info(f"Original bbox: {original_bbox}")
        logger.info(f"Processed bbox: {processed_bbox}")

    except Exception as e:
        logger.error(f"Dataset initialization error: {str(e)}")
        import traceback
        traceback.print_exc()