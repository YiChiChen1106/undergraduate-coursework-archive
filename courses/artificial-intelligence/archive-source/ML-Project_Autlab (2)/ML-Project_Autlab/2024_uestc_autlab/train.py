import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split
from model import create_model
from dataset import MyCOCODataset
import os
import time
from datetime import datetime
import logging
import pickle
from collections import defaultdict

def setup_logging(output_dir):
    """Set up logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(output_dir, 'training.log')),
            logging.StreamHandler()
        ]
    )

class AverageMeter(object):
    """Compute and store the average and current value"""
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)

def create_data_loader(train_dataset, config):
    """Create data loader"""
    # Different configuration for Windows system
    is_windows = os.name == 'nt'
    num_workers = 0 if is_windows else min(8, os.cpu_count())
    persistent_workers = False if is_windows else True

    train_loader = DataLoader(
        train_dataset,
        batch_size=config['batch_size'],
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False,
        persistent_workers=persistent_workers
    )

    return train_loader

def train_epoch(model, train_loader, criterion, optimizer, scaler, device, epoch, scheduler=None):
    """Train for one epoch"""
    model.train()
    losses = AverageMeter('Loss', ':.4e')
    top1 = AverageMeter('Acc@1', ':6.2f')
    batch_time = AverageMeter('Time', ':6.3f')
    
    # Track accuracy for each class
    class_correct = defaultdict(int)
    class_total = defaultdict(int)
    
    end = time.time()
    
    for i, (images, labels, weights) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        weights = weights.to(device)

        # Calculate batch weights
        batch_weights = weights / weights.sum()

        optimizer.zero_grad()

        with autocast():
            outputs = model(images)
            loss = criterion(outputs, labels)  # [batch_size]
            weighted_loss = (loss * batch_weights).mean()  # Calculate weighted average loss

        # Gradient clipping
        scaler.scale(weighted_loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        scaler.step(optimizer)
        scaler.update()

        if scheduler is not None:
            scheduler.step()

        # Calculate accuracy
        _, predicted = outputs.max(1)
        correct = predicted.eq(labels)
        acc = correct.float().mean() * 100

        # Update class-wise accuracy
        for label, is_correct in zip(labels, correct):
            class_total[label.item()] += 1
            if is_correct:
                class_correct[label.item()] += 1

        # Update meters
        losses.update(weighted_loss.item(), images.size(0))
        top1.update(acc.item(), images.size(0))
        batch_time.update(time.time() - end)
        end = time.time()

        # Print training status
        if i % 10 == 0:
            logging.info(
                'Epoch: [{0}][{1}/{2}]\t'
                'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                'Acc@1 {top1.val:.3f} ({top1.avg:.3f})'.format(
                    epoch, i, len(train_loader), batch_time=batch_time,
                    loss=losses, top1=top1))

    # Output accuracy for each class
    logging.info("\nClass-wise Training Accuracies:")
    for cls in sorted(class_total.keys()):
        if class_total[cls] > 0:
            cls_acc = 100.0 * class_correct[cls] / class_total[cls]
            category_name = train_loader.dataset.dataset.categories[cls]
            logging.info(f'{category_name:15s}: {cls_acc:.2f}% ({class_correct[cls]}/{class_total[cls]})')

    return losses.avg, top1.avg

def save_checkpoint(state, is_best, output_dir, epoch):
    """Save checkpoint"""
    filename = os.path.join(output_dir, f'checkpoint_epoch_{epoch}.pth')
    torch.save(state, filename)
    if is_best:
        best_filename = os.path.join(output_dir, 'best_model.pth')
        torch.save(state, best_filename)

def main():
    # Configuration parameters
    config = {
        'data_root': "C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/coco",
        'annofile': "C:/Users/28100/Desktop/AI/MLproject/ML-Project_Autlab/2024_uestc_autlab/coco/annotations.json",
        'lr': 3e-4,
        'min_lr': 1e-6,
        'batch_size': 32,
        'num_classes': 7,
        'num_epochs': 200,
        'weight_decay': 1e-4,
        'model_name': 'efficientnet_b0',
        'dropout_rate': 0.5,
        'output_size': (224, 224),
        'warmup_epochs': 5,
        'seed': 42
    }

    # Set random seed
    torch.manual_seed(config['seed'])
    if torch.cuda.is_available():
        torch.cuda.manual_seed(config['seed'])
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f'outputs/run_{timestamp}'
    os.makedirs(output_dir, exist_ok=True)

    # Setup logging
    setup_logging(output_dir)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")

    # Load dataset
    dataset = MyCOCODataset(
        data_root=config['data_root'],
        annofile=config['annofile'],
        is_train=True,
        output_size=config['output_size']
    )

    # Split dataset (only create test set, not used in training)
    indices = list(range(len(dataset)))
    train_indices, test_indices = train_test_split(
        indices, test_size=0.2, stratify=[dataset[i][1].item() for i in indices],
        random_state=config['seed']
    )

    # Save test indices
    test_indices_path = os.path.join(output_dir, 'test_indices.pkl')
    with open(test_indices_path, 'wb') as f:
        pickle.dump(test_indices, f)
    logging.info(f"Test indices saved to {test_indices_path}")

    # Create training set
    train_dataset = Subset(dataset, train_indices)

    # Create data loader
    train_loader = create_data_loader(train_dataset, config)

    logging.info(f"\nDataset split:")
    logging.info(f"Training set: {len(train_dataset)} samples")
    logging.info(f"Test set: {len(test_indices)} samples")

    # Create model
    model = create_model(config)
    model = model.to(device)

    if torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)

    # Get layer groups for differential learning rates
    layer_groups = model.module.get_layer_groups() if isinstance(model, nn.DataParallel) else model.get_layer_groups()

    # Optimizer
    optimizer = optim.AdamW(layer_groups, lr=config['lr'], weight_decay=config['weight_decay'])

    # Learning rate scheduling
    num_training_steps = len(train_loader) * config['num_epochs']
    num_warmup_steps = len(train_loader) * config['warmup_epochs']

    scheduler = optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=config['lr'],
        total_steps=num_training_steps,
        pct_start=num_warmup_steps/num_training_steps,
        anneal_strategy='cos',
        final_div_factor=config['lr']/config['min_lr']
    )

    # Loss function
    class_weights = dataset.class_weights.to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, reduction='none')

    # Mixed precision training
    scaler = GradScaler()

    # Training loop
    best_acc = 0
    best_epoch = 0
    early_stopping_counter = 0
    early_stopping_patience = 15

    try:
        for epoch in range(config['num_epochs']):
            logging.info(f"\nEpoch {epoch+1}/{config['num_epochs']}")
            logging.info('-' * 60)

            # Training phase
            train_loss, train_acc = train_epoch(
                model, train_loader, criterion, optimizer, scaler, device, epoch, scheduler
            )

            # Record learning rate
            current_lr = optimizer.param_groups[0]['lr']
            logging.info(f'Current LR: {current_lr:.6f}')
            logging.info(f'Training Loss: {train_loss:.4f}, Accuracy: {train_acc:.2f}%')

            # Check for best model
            is_best = train_acc > best_acc
            if is_best:
                best_acc = train_acc
                best_epoch = epoch
                early_stopping_counter = 0
                logging.info(f'New best model training accuracy: {best_acc:.2f}%')
            else:
                early_stopping_counter += 1
                logging.info(f'No improvement for {early_stopping_counter} epochs')

            # Save checkpoint
            if isinstance(model, nn.DataParallel):
                model_state_dict = model.module.state_dict()
            else:
                model_state_dict = model.state_dict()

            save_checkpoint({
                'epoch': epoch,
                'model_state_dict': model_state_dict,
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_acc': best_acc,
                'config': config
            }, is_best, output_dir, epoch)

            # Early stopping
            if early_stopping_counter >= early_stopping_patience:
                logging.info(f'Early stopping triggered after {early_stopping_patience} epochs without improvement')
                break

        logging.info(f'\nTraining completed!')
        logging.info(f'Best training accuracy: {best_acc:.2f}% at epoch {best_epoch+1}')

    except KeyboardInterrupt:
        logging.info('\nTraining interrupted by user')
        if best_acc > 0:
            logging.info(f'Best training accuracy achieved: {best_acc:.2f}% at epoch {best_epoch+1}')
    except Exception as e:
        logging.error(f'Training failed: {str(e)}')
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        import traceback
        traceback.print_exc()