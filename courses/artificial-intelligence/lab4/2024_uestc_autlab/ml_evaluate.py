import pickle
import sys
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split
import numpy as np

sys.path.append("./")
from dataset import MyCOCODataset
from mlmodel import Model  # Adjusted path import to match project structure

classes = 7  # Number of classes in the dataset


def confusion_matrix(predicted, ground_truth, num_classes):
    """
    Calculate the confusion matrix.
    """
    matrix = np.zeros(shape=(num_classes, num_classes), dtype=int)
    for p, g in np.stack([predicted, ground_truth], axis=1):
        matrix[g, p] += 1  # Rows correspond to ground truth; columns to predictions
    return matrix


def main():
    # Load trained model
    model: Model = pickle.load(open(r"outputs/model.pkl", "rb"))

    # Load entire dataset
    dataset = MyCOCODataset(
        "data/Combined_COCO_Dataset/coco",  # Path to the data folder
        "data/Combined_COCO_Dataset/coco/annotations.json",
        output_size=(128, 128),
    )

    # Split dataset into train_set (80%) and test_set (20%)
    indices = list(range(len(dataset)))  # Get indices for all samples
    _, test_indices = train_test_split(indices, test_size=0.2, random_state=42)  # Use the same split as in train.py
    test_set = Subset(dataset, test_indices)  # Create test subset

    # Prepare data loader for the test set
    loader = DataLoader(
        test_set, batch_size=32, num_workers=0, collate_fn=model._collate_fn
    )

    # Collect predictions and ground truth
    test_predicted = []
    test_ground_truth = []
    for imgs, cats in loader:
        result = model.forward(imgs)  # Perform prediction
        test_predicted.append(result)
        test_ground_truth.append(cats)

    # Concatenate results
    test_predicted = np.concatenate(test_predicted)
    test_ground_truth = np.concatenate(test_ground_truth)

    # Compute confusion matrix
    matrix = confusion_matrix(test_predicted, test_ground_truth, classes)

    # Print confusion matrix
    print("Confusion Matrix:")
    print(matrix)


if __name__ == "__main__":
    main()
