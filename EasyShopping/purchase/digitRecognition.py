from torchvision import datasets
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
from PIL import Image
import tensorflow as tf
import cv2
import numpy as np

train_data = datasets.MNIST(root = 'data',
                            train = True,
                            transform = ToTensor(),
                            download = True)

test_data = datasets.MNIST(root = 'data',
                           train = False,
                           transform = ToTensor(),
                           download = True)

# Shape and label of the training images
# print(f'Train Data Shape: {train_data.data.shape}') # torch.Size([60000, 28, 28])
# print(f'Train Targets Shape: {train_data.targets.shape}') # torch.Size([60000])
# print('Sample Training Labels:', train_data.targets) # tensor([5, 0, 4,  ..., 5, 6, 8])

# First image from train_data
# image, label = train_data[0] 
# print('First Train Image Shape: {image.shape}') # torch.Size([1, 28, 28])
# print('First Train Label: {label}') # 5

# Shape and label of the test images
# print(f'Test Data Shape: {test_data.data.shape}') # torch.Size([10000, 28, 28])
# print(f'Test Targets Shape: {test_data.targets.shape}') # tensor.Size([10000])
# print('Sample Test Labels:', test_data.targets) # tensor([5, 0, 4,  ..., 5, 6, 8])

# First image from test_data
# image, label = test_data[0]
# print('First Test Image Shape: {image.shape}') # torch.Size([1, 28, 28])
# print('First Test Label: {label}') # 7

#DataLoader: manage loading data in batches and can perform shuffling of the data in each epoch
loaders = {
    'train': DataLoader(train_data, 
                        batch_size = 100,
                        shuffle = True, # data will be shuffled randomly before being divided into batches
                        num_workers = 1), # number of threads used to load data
    'test': DataLoader(test_data,
                       batch_size = 100,
                       shuffle = True,
                       num_workers = 1)
}

# Shape of 1 batch 
# for batch_idx, (data, target) in enumerate(loaders['train']):
#     print(f"Train Batch {batch_idx + 1}: Data Shape = {data.shape}, Target Shape = {target.shape}")
#     break

# for batch_idx, (data, target) in enumerate(loaders['test']):
#     print(f"Test Batch {batch_idx + 1}: Data Shape = {data.shape}, Target Shape = {target.shape}")
#     break

# Loop through 5 images in training dataset
# fig = plt.figure(figsize = (20, 10))
# for i in range(1, 6):
#     img = transforms.ToPILImage(mode = 'L')(train_data[i][0]) #(1, 28, 28) -> (28, 28)
#     fig.add_subplot(1, 5, i)
#     plt.title(f'Label: {train_data[i][1].item()}')
#     plt.imshow(img, cmap='gray')

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        # Lớp tích chập đầu tiên với Batch Normalization
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5)  # 1 kênh đầu vào, 32 kênh đầu ra
        self.bn1 = nn.BatchNorm2d(32)  # Batch Normalization cho lớp conv1
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5)  # 32 kênh đầu vào, 64 kênh đầu ra
        self.bn2 = nn.BatchNorm2d(64)  # Batch Normalization cho lớp conv2
        self.fc1 = nn.Linear(64 * 4 * 4, 128)  # Kích thước đầu vào đã được điều chỉnh
        self.fc2 = nn.Linear(128, 10)  # 128 đầu vào, 10 đầu ra cho 10 lớp

        self.dropout = nn.Dropout(0.5)  # Tỷ lệ dropout 50%

    def forward(self, x):
        # Lớp tích chập đầu tiên
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2)  # Max pooling với kích thước 2x2

        # Lớp tích chập thứ hai
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2)  # Max pooling với kích thước 2x2

        # Chuyển đổi kích thước để vào lớp fully connected
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))  # Lớp fully connected đầu tiên
        x = self.dropout(x)  # Áp dụng dropout
        x = self.fc2(x)  # Lớp fully connected cuối cùng

        return x
  
model = CNN()
optimizer = optim.Adam(model.parameters(), lr = 0.001)
loss_fn = nn.CrossEntropyLoss()

def train(epoch):
    model.train()  # Đặt mô hình ở chế độ huấn luyện
    for batch_idx, (data, target) in enumerate(loaders['train']):
        optimizer.zero_grad()  # Đặt lại gradient
        output = model(data)  # Forward pass
        loss = loss_fn(output, target)  # Tính toán mất mát
        loss.backward()  # Backward pass
        optimizer.step()  # Cập nhật trọng số

        if batch_idx % 20 == 0:
            print(f'Train epoch: {epoch} | [{batch_idx * len(data)} / {len(loaders["train"].dataset)} '
                    f'({100. * batch_idx / len(loaders["train"].dataset):.0f}%)]\tLoss: {loss.item():.6f}')

def test():
    model.eval()  # Đặt mô hình ở chế độ kiểm tra
    test_loss = 0
    correct = 0

    with torch.no_grad():  # Tắt gradient
        for data, target in loaders['test']:
            output = model(data)  # Forward pass
            test_loss += loss_fn(output, target).item()  # Tính tổng mất mát
            pred = output.argmax(dim=1, keepdim=True)  # Dự đoán lớp
            correct += pred.eq(target.view_as(pred)).sum().item()  # Tính số lượng dự đoán đúng

    test_loss /= len(loaders['test'])  # Tính trung bình mất mát
    print(f'\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(loaders["test"].dataset)} '
          f'({100. * correct / len(loaders["test"].dataset):.2f}%)\n')

for epoch in range(1, 11):
    train(epoch)
    test()

model.eval()
data, target = test_data[5]
data = data.unsqueeze(0)
output = model(data)
prediction = output.argmax(dim = 1, keepdim = True).item()
print(f"Prediction: {prediction}")
image = data.squeeze(0).squeeze(0).numpy()
plt.imshow(image, cmap = 'gray')
plt.show()

img_size = 28
def predict_image(model, image):
    model.eval()
    with torch.no_grad():
        output = model(image.unsqueeze(0))
        _, predicted = torch.max(output.data, 1)
        return predicted.item()
  
# img_path = '/content/drive/MyDrive/Data/Screenshot 2024-04-01 235037.png'
# image = cv2.imread(img_path)
# plt.imshow(image)
# print(image.shape)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# resize = cv2.resize(gray, (28, 28), interpolation = cv2.INTER_AREA)
# print(resize.shape)
# newing = tf.keras.utils.normalize(resize, axis = 1)
# newing = np.array(newing).reshape(1, img_size, img_size)
# newing = newing.astype(np.float32)
# print(newing.shape)
# img_tensor = torch.tensor(newing)
# result = predict_image(model, img_tensor)
# print(result)