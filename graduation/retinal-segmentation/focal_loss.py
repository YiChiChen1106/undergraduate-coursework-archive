import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLossForSegmentation(nn.Module):
    """
    Focal Loss for multi-class segmentation tasks.
    Assumes input logits are of shape (B, C, H, W, [D]) and target is (B, 1, H, W, [D]).
    """
    def __init__(self, alpha=0.25, gamma=2.0, reduction='mean', ignore_index=None):
        super().__init__()
        self.alpha = alpha # Can be None or a float for binary/multi-class alpha weighting
        self.gamma = gamma
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, logits, target):
        # logits: (B, C, Spatial...), target: (B, 1, Spatial...)
        num_classes = logits.shape[1]

        # Apply softmax to get probabilities
        probs = F.softmax(logits, dim=1)

        # One-hot encode the target, necessary for calculating pt
        target_one_hot = F.one_hot(target.squeeze(1), num_classes=num_classes).permute(0, -1, *range(1, target.ndim -1)).float()
        # Shape becomes (B, C, Spatial...)

        # Calculate pt (probability of the ground truth class)
        pt = torch.sum(probs * target_one_hot, dim=1, keepdim=True) # (B, 1, Spatial...)
        # Prevent nan/inf
        pt = torch.clamp(pt, 1e-9, 1.0 - 1e-9)

        # Calculate the actual focal loss
        focal_term = (1 - pt) ** self.gamma
        ce_term = -torch.log(pt) # This is CrossEntropy for the correct class

        # Alpha weighting (optional)
        if self.alpha is not None:
            # Simple alpha weighting: weight positive predictions
            # More complex alpha could weight each class differently
            alpha_weight = torch.ones_like(target_one_hot) * (1 - self.alpha)
            alpha_weight = torch.where(target_one_hot == 1, self.alpha, alpha_weight)
            # Apply alpha weight to the cross-entropy term before combining
            # Note: This simple alpha is more suited for binary/imbalanced foreground
            # For multi-class, you might need a per-class alpha tensor
            loss = alpha_weight * focal_term * ce_term # Apply alpha here
        else:
            loss = focal_term * ce_term

        # Handle ignore_index (mask out ignored pixels)
        if self.ignore_index is not None:
            # Create a mask where target is not the ignore_index
            # target shape is (B, 1, Spatial...)
            valid_mask = (target != self.ignore_index) # (B, 1, Spatial...)
            loss = loss * valid_mask
            # Count only valid pixels for reduction
            num_valid_pixels = valid_mask.sum()

        # Apply reduction
        if self.reduction == 'mean':
            if self.ignore_index is not None and num_valid_pixels > 0:
                 loss = loss.sum() / num_valid_pixels
            elif self.ignore_index is not None: # All pixels ignored
                 loss = torch.tensor(0.0, device=logits.device, dtype=logits.dtype)
            else:
                 loss = loss.mean()
        elif self.reduction == 'sum':
            loss = loss.sum()

        return loss