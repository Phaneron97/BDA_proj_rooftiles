# -*- coding: utf-8 -*-
"""efficient_net_b1_train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fjFF6bKH7EgYzHaBf3y9Yz-Cv8unH2wU
"""

train_ratio = 0.7
learning_rate = 0.001
number_of_train_epochs = 10
all_folders = ['d0000_b_blw_g_OVH',
 'd0000_o_blw_g_OVH',
 'd0001_b_blw_n_TDN44',
 'd0001_o_blw_n_TDN44',
 'd0002_b_nrd_g_VH',
 'd0002_o_nrd_g_VH',
 'd0003_b_ord_n_NS',
 'd0003_o_ord_n_NS',
 'd0004_b_mzv_n_OVHvario',
 'd0004_o_mzv_n_OVHvario',
 'd0005_b_nrd_n_OVH200',
 'd0005_o_nrd_n_OVH200',
 'd0006_b_blw_g_OH',
 'd0006_o_blw_g_OH',
 'd0007_b_nrd_n_VHm6',
 'd0007_o_nrd_n_VHm6',
 'd0008_b_rnd_g_ov_o&z',
 'd0008_o_rnd_g_ov_o&z']

four_folders = ['d0000_b_blw_g_OVH',
 'd0001_b_blw_n_TDN44',
 'd0002_b_nrd_g_VH',
 'd0003_b_ord_n_NS',
 ]
two_folders = ['d0000_b_blw_g_OVH',
 'd0001_b_blw_n_TDN44',
 ]
# Define dataset and data loaders
pathToDateset = '/content/drive/MyDrive/MinorBigData/Project/dataset_sample'
folders_to_use = all_folders # Specify the folders you want to consider

# %% imports
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image

# %% dataset class
# Define dataset class
class RooftileDataset(Dataset):
    def __init__(self, root_dir, folders, transform=None):
        self.root_dir = root_dir
        self.folders = folders
        self.transform = transform
        self.classes = sorted(self.folders)

        self.class_images = []
        self.total_images = 0
        for class_folder in self.folders:
            class_path = os.path.join(self.root_dir, class_folder)
            class_files = os.listdir(class_path)
            self.class_images.append({
                'class_folder': class_folder,
                'images': class_files
            })
            print(f'Read {len(class_files)} from {class_folder}')
            self.total_images += len(class_files)

    def __len__(self):
        return self.total_images

    def __getitem__(self, idx):
        class_idx = idx % len(self.classes)
        selected_class = self.class_images[class_idx]
        class_path = os.path.join(self.root_dir, selected_class['class_folder'])
        img_name = selected_class['images'][idx // len(self.classes)]
        img_path = os.path.join(class_path, img_name)
        # image = torchvision.io.read_image(img_path)
        image = Image.open(img_path).convert("RGB")
        label = class_idx
        if self.transform:
            image = self.transform(image)
        return image, label

# %% creating train and test datasets
# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = RooftileDataset(root_dir=pathToDateset, folders=folders_to_use, transform=transform)

# Split dataset into train and test
train_size = int(train_ratio * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

print(f'Number of classes={len(dataset.classes)}, number of train={train_size}, number of test={test_size}')

# %% loading Efficient Net model
# Load pre-trained EfficientNet model
# efficientnet_b{0-7} available.
print('loading efficient net')
model_name = "efficientnet_b1"
weights = torchvision.models.EfficientNet_B1_Weights
model = torchvision.models.efficientnet_b1(weights=weights, progress=True)

# Freeze convolutional layers
for param in model.features.parameters():
    param.requires_grad = False

# Modify the fully connected layers for the number of classes
num_classes = len(dataset.classes)
model.classifier[1] = nn.Linear(1280, num_classes)
print(model)
# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f'deice={device}')
num_epochs = number_of_train_epochs

# %% train
for epoch in range(num_epochs):
    print(f"starting epoch {epoch}")
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_accuracy = 100 * correct / total
    train_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1}, Training Loss: {train_loss}, Training Accuracy: {train_accuracy}%")

# %% test
# Test loop
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Result of {model_name} test:")
print(f"random accuracy = {100/num_classes}")
print(f"Test Accuracy: {100 * correct / total}%")
#Result of efficientnet_b1 test:
#random accuracy = 5.555555555555555
#Test Accuracy: 67.88990825688073%

