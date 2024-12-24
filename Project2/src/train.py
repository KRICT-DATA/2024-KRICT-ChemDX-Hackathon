import numpy as np
import torch
# from sklearn.model_selection import train_test_split
import torch.nn as nn
from torch import nn
from torch.utils.data import Dataset


class ProcessedDataDataset(Dataset):
    def __init__(self, data):
        self.data_keys = list(data.keys())
        self.data = data

    def __len__(self):
        return len(self.data_keys)

    def __getitem__(self, idx):
        data_id = self.data_keys[idx]
        sample = self.data[data_id]

        descriptor = torch.tensor(sample["descriptor"], dtype=torch.float32)
        descriptor_2 = torch.tensor(sample['descriptor_2'], dtype=torch.float32)
        natoms = torch.tensor(sample["natoms"], dtype=torch.int)
        value_per_atom = torch.tensor([sample["value_per_atom"]], dtype=torch.float32)
        # value = torch.tensor([sample["value"]], dtype=torch.float32)

        # Exclude atoms from the returned dictionary
        return {
            "id": data_id,
            "descriptor": descriptor,
            "descriptor_2": descriptor_2,
            "natoms": natoms,
            "value_per_atom": value_per_atom,
            # "value": value
        }


def train_val_test_split_indices(dataset, train_size=0.7, val_size=0.15, test_size=0.15, random_seed=42):
    """
    Split dataset indices into train, validation, and test sets.

    Args:
        dataset (Dataset): The dataset to split.
        train_size (float): Proportion of data for the training set.
        val_size (float): Proportion of data for the validation set.
        test_size (float): Proportion of data for the test set.
        random_seed (int): Seed for reproducibility.

    Returns:
        tuple: Three lists containing train, validation, and test indices.
    """
    # Check that split sizes add up to 1
    assert train_size + val_size + test_size == 1, "Split sizes must add up to 1."

    # Set random seed and shuffle indices
    np.random.seed(random_seed)
    indices = np.arange(len(dataset))
    np.random.shuffle(indices)

    # Calculate split points
    train_split = int(len(indices) * train_size)
    val_split = int(len(indices) * (train_size + val_size))

    # Split indices
    train_indices = indices[:train_split]
    val_indices = indices[train_split:val_split]
    test_indices = indices[val_split:]

    return train_indices, val_indices, test_indices


class Model(nn.Module):
    def __init__(self, feat_dim=256, n_emb=64, n_dimensions=64, mean: float = 0.0, std: float = 1.0):
        super().__init__()
        self.mlp_emb = nn.Sequential(
            nn.Linear(feat_dim, n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions, n_emb),
        )
        self.mlp_fit = nn.Sequential(
            nn.Linear(n_emb, n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions,n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions,n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions, 1)
        )
        self.register_buffer('mean', torch.tensor(mean, dtype=torch.float32))
        self.register_buffer('std', torch.tensor(std, dtype=torch.float32))

    def forward(self, descriptor):
        emb = self.mlp_emb(descriptor)
        output = self.mlp_fit(emb)
        self.mean = self.mean.to(descriptor.device)
        self.std = self.std.to(descriptor.device)
        output = output * self.std + self.mean
        return output

class Model2(nn.Module):
    def __init__(self, n_emb=64, n_dimensions=64, mean: float = 0.0, std: float = 1.0):
        super().__init__()

        self.mlp_fit = nn.Sequential(
            nn.Linear(n_emb, n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions,n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions,n_dimensions),
            nn.ReLU(),
            nn.Linear(n_dimensions, 1)
        )
        self.register_buffer('mean', torch.tensor(mean, dtype=torch.float32))
        self.register_buffer('std', torch.tensor(std, dtype=torch.float32))

    def forward(self, descriptor):
        # emb = self.mlp_emb(descriptor)
        output = self.mlp_fit(descriptor)
        self.mean = self.mean.to(descriptor.device)
        self.std = self.std.to(descriptor.device)
        output = output * self.std + self.mean
        return output


class Trainer:
    def __init__(self, model, input_key, train_loader, val_loader, criterion, optimizer, device='cpu'):
        self.input_key = input_key
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device

    def train(self, num_epochs=10):
        self.model.train()
        loss_list = []
        for epoch in range(num_epochs):
            total_loss = 0
            for batch in self.train_loader:
                descriptors = batch[self.input_key].to(self.device)  # Model input
                target = batch['value_per_atom'].to(self.device)  # Assume we are predicting 'value'

                # Forward pass
                outputs = self.model(descriptors)
                loss = self.criterion(outputs, target)  # Calculate loss based on 'value'

                # Backward and optimize
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
            loss_list.append(total_loss)

            avg_loss = total_loss / len(self.train_loader)
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

            # Evaluate on the val set after each epoch
            val_loss = self.evaluate()
            print(f"val Loss after Epoch [{epoch+1}/{num_epochs}]: {val_loss:.4f}")
        return loss_list

    def evaluate(self):
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for batch in self.val_loader:
                descriptors = batch[self.input_key].to(self.device)
                target = batch['value_per_atom'].to(self.device)

                outputs = self.model(descriptors)
                loss = self.criterion(outputs, target)
                total_loss += loss.item()

        avg_loss = total_loss / len(self.val_loader)
        return avg_loss


def evaluate(model, input_key, test_loader, device):
    model.eval()
    pred_list = []
    targ_list = []
    with torch.no_grad():
        for batch in test_loader:
            descriptors = batch[input_key].to(device)
            target = batch['value_per_atom'].to(device)

            outputs = model(descriptors)
            pred_list.append(outputs)
            targ_list.append(target)
    return torch.cat(pred_list).numpy(), torch.cat(targ_list).numpy()
