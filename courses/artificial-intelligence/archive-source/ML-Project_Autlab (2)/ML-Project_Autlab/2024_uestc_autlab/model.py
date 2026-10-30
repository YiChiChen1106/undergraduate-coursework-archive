import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import logging

logger = logging.getLogger(__name__)

class SEBlock(nn.Module):
    """Squeeze-and-Excitation Block"""
    def __init__(self, channels, reduction=16):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class ImprovedModel(nn.Module):
    def __init__(self, num_classes=7, model_name='efficientnet_b0', dropout_rate=0.5):
        super(ImprovedModel, self).__init__()
        self.model_name = model_name
        self.num_classes = num_classes
        self.dropout_rate = dropout_rate

        # Load pretrained model
        if model_name == 'efficientnet_b0':
            self.base_model = models.efficientnet_b0(pretrained=True)
            num_ftrs = self.base_model.classifier[1].in_features
            # Keep features only
            self.base_model = self.base_model.features

            # Freeze early layers
            for param in self.base_model[:-4].parameters():
                param.requires_grad = False

        elif model_name == 'resnet50':
            self.base_model = models.resnet50(pretrained=True)
            num_ftrs = self.base_model.fc.in_features
            # Remove the final FC layer but keep conv layers
            self.base_model = nn.Sequential(*list(self.base_model.children())[:-2])

            # Freeze except last block
            for name, param in self.base_model.named_parameters():
                if 'layer4' not in name:
                    param.requires_grad = False
        else:
            raise ValueError(f"Unsupported model name: {model_name}")

        # Feature extractor
        self.feature_extractor = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(p=0.2),
            nn.Linear(num_ftrs, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate)
        )

        # Classifier
        self.classifier = nn.Linear(512, num_classes)

        # Initialize weights
        self._initialize_weights()
        
        # Print model info
        self._print_model_info(num_ftrs)

    def _initialize_weights(self):
        """Initialize network weights"""
        for m in self.feature_extractor.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

        nn.init.xavier_normal_(self.classifier.weight)
        if self.classifier.bias is not None:
            nn.init.constant_(self.classifier.bias, 0)

    def _print_model_info(self, num_ftrs):
        """Print model architecture and parameters information"""
        logger.info(f"\nModel Configuration:")
        logger.info(f"Base Model: {self.model_name}")
        logger.info(f"Number of classes: {self.num_classes}")
        logger.info(f"Feature dimension: {num_ftrs}")
        logger.info(f"Dropout rate: {self.dropout_rate}")
        
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        logger.info(f"Total parameters: {total_params:,}")
        logger.info(f"Trainable parameters: {trainable_params:,}")

    def forward(self, x):
        """Forward pass through the network"""
        # Extract features - will maintain spatial dimensions
        features = self.base_model(x)
        # Process features
        features = self.feature_extractor(features)
        # Classify
        out = self.classifier(features)
        return out

    def get_features(self, x):
        """Extract feature representations from input"""
        features = self.base_model(x)
        return self.feature_extractor(features)

    def unfreeze_layers(self, num_layers=3):
        """Unfreeze specified number of layers for fine-tuning"""
        if self.model_name == 'efficientnet_b0':
            layers = list(self.base_model.children())
            for layer in layers[-num_layers:]:
                for param in layer.parameters():
                    param.requires_grad = True
        elif self.model_name == 'resnet50':
            layers_to_unfreeze = [f'layer{i}' for i in range(5-num_layers, 5)]
            for name, param in self.base_model.named_parameters():
                if any(layer in name for layer in layers_to_unfreeze):
                    param.requires_grad = True

        logger.info(f"Unfroze last {num_layers} layers")

    def get_layer_groups(self):
        """Get layer groups for differential learning rates optimization"""
        if self.model_name == 'efficientnet_b0':
            return [
                {'params': list(self.base_model[-4:].parameters()), 'lr_mult': 0.1},
                {'params': self.feature_extractor.parameters(), 'lr_mult': 0.5},
                {'params': self.classifier.parameters(), 'lr_mult': 1.0}
            ]
        elif self.model_name == 'resnet50':
            return [
                {'params': self.base_model[-1].parameters(), 'lr_mult': 0.1},
                {'params': self.feature_extractor.parameters(), 'lr_mult': 0.5},
                {'params': self.classifier.parameters(), 'lr_mult': 1.0}
            ]

def create_model(model_config):
    """Create model instance based on configuration"""
    model = ImprovedModel(
        num_classes=model_config.get('num_classes', 7),
        model_name=model_config.get('model_name', 'efficientnet_b0'),
        dropout_rate=model_config.get('dropout_rate', 0.5)
    )
    return model

if __name__ == "__main__":
    # Test model functionality
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        
        # Create model instance
        model_config = {
            'num_classes': 7,
            'model_name': 'efficientnet_b0',
            'dropout_rate': 0.5
        }
        model = create_model(model_config)

        # Test forward pass
        x = torch.randn(4, 3, 224, 224)  # batch size of 4
        output = model(x)
        logger.info(f"\nInput shape: {x.shape}")
        logger.info(f"Output shape: {output.shape}")

        # Test feature extraction
        features = model.get_features(x)
        logger.info(f"Feature shape: {features.shape}")

        # Test layer groups
        layer_groups = model.get_layer_groups()
        logger.info("\nLayer groups for optimizer:")
        for idx, group in enumerate(layer_groups):
            logger.info(f"Group {idx}: LR multiplier = {group['lr_mult']}")

    except Exception as e:
        logger.error(f"Model testing error: {str(e)}")
        import traceback
        traceback.print_exc()