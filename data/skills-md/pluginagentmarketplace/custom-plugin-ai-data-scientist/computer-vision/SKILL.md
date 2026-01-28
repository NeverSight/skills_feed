---
name: computer-vision
description: Image processing, object detection, segmentation, and vision models. Use for image classification, object detection, or visual analysis tasks.
sasmp_version: "1.3.0"
bonded_agent: 04-machine-learning-ai
bond_type: SECONDARY_BOND
---

# Computer Vision

Build models to analyze and understand visual data.

## Quick Start

### Image Classification
```python
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# Load pre-trained model
model = models.resnet50(pretrained=True)
model.eval()

# Preprocess image
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

img = Image.open('image.jpg')
img_tensor = transform(img).unsqueeze(0)

# Predict
with torch.no_grad():
    output = model(img_tensor)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top5 = torch.topk(probabilities, 5)

print(top5)
```

### Custom CNN
```python
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
```

## Data Augmentation

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.1
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
```

## Object Detection with YOLO

```python
from ultralytics import YOLO

# Load model
model = YOLO('yolov8n.pt')

# Predict
results = model('image.jpg')

# Process results
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        confidence = box.conf[0]
        class_id = box.cls[0]
        print(f"Class: {class_id}, Confidence: {confidence:.2f}")
        print(f"Box: ({x1}, {y1}, {x2}, {y2})")

# Save results
results[0].save('output.jpg')
```

## Image Segmentation

```python
# Semantic segmentation with DeepLab
model = torch.hub.load(
    'pytorch/vision:v0.10.0',
    'deeplabv3_resnet50',
    pretrained=True
)
model.eval()

# Preprocess
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

input_tensor = preprocess(img).unsqueeze(0)

# Predict
with torch.no_grad():
    output = model(input_tensor)['out'][0]
    output_predictions = output.argmax(0)
```

## Transfer Learning

```python
from torchvision import models

# Load pre-trained ResNet
model = models.resnet50(pretrained=True)

# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# Replace final layer
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)

# Train only final layer
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
```

## Image Processing with OpenCV

```python
import cv2

# Read image
img = cv2.imread('image.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Edge detection
edges = cv2.Canny(gray, 100, 200)

# Blur
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# Resize
resized = cv2.resize(img, (224, 224))

# Draw rectangle
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Save
cv2.imwrite('output.jpg', img)
```

## Face Detection

```python
# Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

## Common Architectures

**Image Classification:**
- ResNet: Skip connections, deep networks
- EfficientNet: Compound scaling, efficient
- Vision Transformer (ViT): Attention-based

**Object Detection:**
- YOLO: Real-time, one-stage
- Faster R-CNN: Two-stage, accurate
- RetinaNet: Focal loss, handles class imbalance

**Segmentation:**
- U-Net: Encoder-decoder, medical imaging
- DeepLab: Atrous convolution, semantic segmentation
- Mask R-CNN: Instance segmentation

## Tips

1. Use pre-trained models for transfer learning
2. Apply data augmentation to prevent overfitting
3. Normalize images (ImageNet statistics)
4. Use appropriate loss functions (CrossEntropy, Focal Loss)
5. Monitor training with visualization
6. Test on diverse images
