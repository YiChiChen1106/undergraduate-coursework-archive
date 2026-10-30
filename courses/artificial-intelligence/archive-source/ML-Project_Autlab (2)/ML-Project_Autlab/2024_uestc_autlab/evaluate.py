import os
import json
import logging
import pickle
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from dataset import MyCOCODataset
from model import create_model

def setup_logging(output_dir):
    """Set up logging"""
    os.makedirs(output_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(output_dir, 'evaluation.log')),
            logging.StreamHandler()
        ]
    )

def create_data_loader(dataset, indices, batch_size):
    """Create data loader"""
    # Ensure all indices are within valid range
    valid_indices = [idx for idx in indices if idx < len(dataset)]
    logging.info(f"Original indices count: {len(indices)}")
    logging.info(f"Valid indices count: {len(valid_indices)}")
    logging.info(f"Dataset length: {len(dataset)}")
    
    if len(valid_indices) != len(indices):
        logging.warning(f"Removed {len(indices) - len(valid_indices)} invalid indices")
    
    if len(valid_indices) == 0:
        logging.error("No valid indices found!")
        raise ValueError("No valid indices for creating DataLoader")
    
    test_dataset = Subset(dataset, valid_indices)
    
    # Different configuration for Windows system
    is_windows = os.name == 'nt'
    num_workers = 0 if is_windows else min(8, os.cpu_count())
    persistent_workers = False if is_windows else True
    
    loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=persistent_workers
    )
    
    logging.info(f"Created DataLoader with {len(loader)} batches")
    return loader

def load_model(model_path, config, device):
    """Load model"""
    model = create_model(config)
    checkpoint = torch.load(model_path, map_location=device)
    
    # Check if DataParallel was used
    state_dict = checkpoint['model_state_dict']
    if list(state_dict.keys())[0].startswith('module.'):
        model = nn.DataParallel(model)
    
    model.load_state_dict(state_dict)
    model = model.to(device)
    model.eval()
    return model

def evaluate_model(model, test_loader, device):
    """Evaluate model"""
    all_preds = []
    all_labels = []
    total_correct = 0
    total_samples = 0
    
    try:
        with torch.no_grad():
            for i, batch in enumerate(test_loader):
                logging.info(f"Processing batch {i+1}/{len(test_loader)}")
                
                if len(batch) == 3:  # If batch contains weights
                    images, labels, _ = batch
                else:  # If batch only contains images and labels
                    images, labels = batch
                
                logging.info(f"Batch size: {images.size(0)}")
                logging.info(f"Labels in batch: {labels.tolist()}")
                
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                
                logging.info(f"Predictions in batch: {predicted.tolist()}")
                
                total_samples += labels.size(0)
                total_correct += (predicted == labels).sum().item()
                
                # Convert to numpy and store
                batch_preds = predicted.cpu().numpy()
                batch_labels = labels.cpu().numpy()
                
                all_preds.extend(batch_preds)
                all_labels.extend(batch_labels)
                
                # Record current batch accuracy
                batch_acc = 100 * (predicted == labels).sum().item() / labels.size(0)
                logging.info(f"Batch {i+1} accuracy: {batch_acc:.2f}%")
        
        logging.info(f"Evaluation completed. Total samples processed: {total_samples}")
        logging.info(f"Total predictions: {len(all_preds)}")
        logging.info(f"Total labels: {len(all_labels)}")
        
        if len(all_preds) == 0:
            logging.error("No predictions were generated!")
            
    except Exception as e:
        logging.error(f"Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return 0.0, [], []
    
    if total_samples == 0:
        logging.error("No samples were processed!")
        return 0.0, [], []
        
    accuracy = 100 * total_correct / total_samples
    return accuracy, all_preds, all_labels

def plot_confusion_matrix(conf_matrix, categories, output_dir):
    """Plot confusion matrix"""
    plt.figure(figsize=(12, 10))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=categories, yticklabels=categories)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
    plt.close()

def main():
    # Configuration
    config = {
        'data_root': "C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/coco",  # Change to COCO root directory
        'annofile': "C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/coco/annotations.json",
        'model_name': 'efficientnet_b0',
        'num_classes': 7,
        'batch_size': 32,
        'output_size': (224, 224)
    }
    
    # Set up output directory and logging
    output_dir = 'evaluation_results'
    setup_logging(output_dir)
    
    try:
        # Set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Using device: {device}")
        
        # Check file paths
        logging.info("Checking file paths...")
        if not os.path.exists(config['data_root']):
            raise FileNotFoundError(f"Data root not found: {config['data_root']}")
        if not os.path.exists(config['annofile']):
            raise FileNotFoundError(f"Annotation file not found: {config['annofile']}")
            
        # Check images folder
        images_dir = os.path.join(config['data_root'], 'JPEGImages').replace('\\', '/')
        logging.info(f"Checking images directory: {images_dir}")
        if not os.path.exists(images_dir):
            raise FileNotFoundError(f"Images directory not found: {images_dir}")
            
        # List some image files as examples
        image_files = os.listdir(images_dir)[:5]
        logging.info(f"Sample image files: {image_files}")
        
        # Check annotations file
        with open(config['annofile'], 'r') as f:
            anno = json.load(f)
            logging.info(f"Annotations info:")
            logging.info(f"Number of images: {len(anno.get('images', []))}")
            logging.info(f"Number of annotations: {len(anno.get('annotations', []))}")
            logging.info(f"Number of categories: {len(anno.get('categories', []))}")
        
        logging.info("Loading dataset...")
        # Load training dataset
        train_dataset = MyCOCODataset(
            data_root=config['data_root'],
            annofile=config['annofile'],
            is_train=True,
            output_size=config['output_size']
        )
        logging.info(f"Training dataset size: {len(train_dataset)}")
        
        # Load test dataset
        dataset = MyCOCODataset(
            data_root=config['data_root'],
            annofile=config['annofile'],
            is_train=False,
            output_size=config['output_size']
        )
        logging.info(f"Test dataset size: {len(dataset)}")
        
        if len(dataset) == 0:
            raise ValueError("Dataset is empty! Please check the data loading process.")
            
        # Load test set indices
        test_indices_path = 'C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/outputs/run_20250107_160049/test_indices.pkl'
        logging.info(f"Loading test indices from {test_indices_path}")
        
        with open(test_indices_path, 'rb') as f:
            test_indices = pickle.load(f)
        
        logging.info(f"Number of test indices: {len(test_indices)}")
        
        # Create data loader
        test_loader = create_data_loader(dataset, test_indices, config['batch_size'])
        logging.info(f"Created test loader with {len(test_loader)} batches")
        
        # Load model
        model_path = 'C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/outputs/run_20250107_160049/best_model.pth'
        logging.info(f"Loading model from {model_path}")
        model = load_model(model_path, config, device)
        
        # Evaluate model
        logging.info("Starting evaluation...")
        accuracy, all_preds, all_labels = evaluate_model(model, test_loader, device)
        logging.info(f"\nTest Accuracy: {accuracy:.2f}%")
        
        # Get category names
        categories = dataset.categories
        logging.info(f"Categories: {categories}")
        
        # Check if predictions exist
        if len(all_preds) == 0 or len(all_labels) == 0:
            logging.error("No predictions or labels available for confusion matrix")
            return
            
        logging.info(f"Number of predictions: {len(all_preds)}")
        logging.info(f"Number of labels: {len(all_labels)}")
        logging.info(f"Label range: {min(all_labels)} to {max(all_labels)}")
        logging.info(f"Prediction range: {min(all_preds)} to {max(all_preds)}")
        
        # Calculate confusion matrix
        conf_matrix = confusion_matrix(all_labels, all_preds)
        logging.info(f"Confusion matrix shape: {conf_matrix.shape}")
        
        if conf_matrix.size > 0:  # Ensure confusion matrix is not empty
            # Plot confusion matrix
            plot_confusion_matrix(conf_matrix, categories, output_dir)
            logging.info(f"Confusion matrix saved to {output_dir}/confusion_matrix.png")
        else:
            logging.error("Empty confusion matrix generated")
        
        # Print detailed classification report
        report = classification_report(
            all_labels, all_preds,
            target_names=categories,
            digits=3
        )
        logging.info("\nClassification Report:\n" + report)
        
        # Calculate accuracy for each class
        class_correct = conf_matrix.diagonal()
        class_total = conf_matrix.sum(axis=1)
        logging.info("\nPer-class accuracy:")
        for i, (correct, total) in enumerate(zip(class_correct, class_total)):
            if total > 0:
                class_acc = 100.0 * correct / total
                logging.info(f'{categories[i]:15s}: {class_acc:.2f}% ({correct}/{total})')
        
    except Exception as e:
        logging.error(f"Evaluation failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()