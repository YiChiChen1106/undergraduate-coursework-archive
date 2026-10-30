from dataset import MyCOCODataset
from mlmodel import Model
from sklearn.model_selection import train_test_split
from torch.utils.data import Subset
import pickle

if __name__ == "__main__":
    # NOTE: loading the dataset here
    dataset = MyCOCODataset(
        "data/Combined_COCO_Dataset/coco",  # Path to the data folder
        "data/Combined_COCO_Dataset/coco/annotations.json",
        output_size=(128, 128),
    )

    # Split dataset into train_set (80%) and test_set (20%)
    indices = list(range(len(dataset)))  # Get indices for all samples
    train_indices, test_indices = train_test_split(indices, test_size=0.2, random_state=42)  # 80% train, 20% test

    train_set = Subset(dataset, train_indices)  # Create training subset
    test_set = Subset(dataset, test_indices)  # Create testing subset

    # Print dataset sizes
    print(f"Total dataset size: {len(dataset)}")
    print(f"Training set size: {len(train_set)}")
    print(f"Test set size: {len(test_set)}")

    # NOTE: create the model
    model = Model(
        hog_cell=16,
        hog_block=4,
        n_components=5,
    )

    # Train the model using the training set
    print("Training PCA model...")
    model.fit_pca(train_set, batch_size=32, num_workers=0)
    print("PCA training completed.")

    print("Training classifier...")
    model.fit_clf(train_set, batch_size=32, num_workers=0)
    print("Classifier training completed.")

    # Save the trained model
    model_path = "outputs/model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print("Model saved to outputs/model.pkl")
