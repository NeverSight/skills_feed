---
name: opencv
description: Open Source Computer Vision Library (OpenCV) for real-time image processing, video analysis, object detection, face recognition, and camera calibration. Use when working with images, videos, cameras, edge detection, contours, feature detection, image transformations, object tracking, optical flow, or any computer vision task.
version: 4.9.0
license: Apache-2.0
---

# OpenCV - Computer Vision and Image Processing

OpenCV (Open Source Computer Vision Library) is the de facto standard library for computer vision tasks. It provides 2500+ optimized algorithms for real-time image and video processing, from basic operations like reading images to advanced tasks like face recognition and 3D reconstruction.

## When to Use

- Reading, writing, and displaying images and videos from files or cameras.
- Image preprocessing (resizing, cropping, rotating, color conversion).
- Edge detection (Canny, Sobel) and contour finding.
- Feature detection and matching (SIFT, ORB, AKAZE).
- Object detection (Haar Cascades, HOG, DNN module for YOLO/SSD).
- Face detection and recognition.
- Image segmentation (thresholding, watershed, GrabCut).
- Video analysis (motion detection, object tracking, optical flow).
- Camera calibration and 3D reconstruction.
- Image stitching and panorama creation.
- Real-time applications requiring fast performance.

## Reference Documentation

**Official docs**: https://docs.opencv.org/4.x/  
**GitHub**: https://github.com/opencv/opencv  
**Tutorials**: https://docs.opencv.org/4.x/d9/df8/tutorial_root.html  
**Search patterns**: `cv2.imread`, `cv2.cvtColor`, `cv2.Canny`, `cv2.findContours`, `cv2.VideoCapture`

## Core Principles

### Image as NumPy Array
OpenCV represents images as NumPy arrays with shape (height, width, channels). This allows seamless integration with NumPy operations and other scientific Python libraries.

### BGR Color Space (Not RGB!)
OpenCV uses BGR (Blue-Green-Red) instead of RGB by default. This is critical to remember when displaying images or integrating with other libraries.

### In-Place vs Copy Operations
Many OpenCV functions modify images in-place for performance. Understanding when copies are made is essential for efficient code.

### C++ Performance in Python
OpenCV is written in optimized C++, making it extremely fast even when called from Python. Avoid Python loops when OpenCV vectorized operations exist.

## Quick Reference

### Installation

```bash
# Basic OpenCV
pip install opencv-python

# With contrib modules (SIFT, SURF, etc.)
pip install opencv-contrib-python

# Headless (no GUI, for servers)
pip install opencv-python-headless
```

### Standard Imports

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

### Basic Pattern - Read, Process, Display

```python
import cv2

# 1. Read image
img = cv2.imread('image.jpg')

# 2. Process (convert to grayscale)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Display
cv2.imshow('Grayscale', gray)
cv2.waitKey(0)  # Wait for key press
cv2.destroyAllWindows()
```

### Basic Pattern - Video Processing

```python
import cv2

# 1. Open video capture
cap = cv2.VideoCapture(0)  # 0 = default camera, or 'video.mp4'

while True:
    # 2. Read frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # 3. Process frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 4. Display
    cv2.imshow('Video', gray)
    
    # 5. Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 6. Cleanup
cap.release()
cv2.destroyAllWindows()
```

## Critical Rules

### ✅ DO

- **Check Image Loaded** - Always verify `img is not None` after `cv2.imread()` to catch file errors.
- **Use cv2.cvtColor() for Color Conversion** - Don't manually rearrange channels; use the provided conversion codes.
- **Release Resources** - Always call `cap.release()` and `cv2.destroyAllWindows()` when done with video/windows.
- **Copy Before Modifying** - Use `img.copy()` if you need to preserve the original image.
- **Use Appropriate Data Types** - Keep images as uint8 (0-255) for display, convert to float32 (0-1) for mathematical operations.
- **Validate VideoCapture** - Check `cap.isOpened()` before reading frames.
- **Use BGR2RGB for Matplotlib** - Convert BGR to RGB when displaying with matplotlib.
- **Vectorize Operations** - Use OpenCV's built-in functions instead of Python loops over pixels.

### ❌ DON'T

- **Don't Assume RGB** - OpenCV uses BGR by default; convert to RGB for matplotlib or PIL.
- **Don't Forget waitKey()** - Without `cv2.waitKey()`, windows won't display properly.
- **Don't Mix PIL and OpenCV Directly** - Convert between them explicitly (OpenCV uses BGR, PIL uses RGB).
- **Don't Process Video in Memory** - Process frame-by-frame to avoid memory issues with large videos.
- **Don't Use Python Loops for Pixels** - This is 100x slower than vectorized operations.
- **Don't Hardcode Paths** - Use `os.path.join()` or `pathlib` for cross-platform compatibility.

## Anti-Patterns (NEVER)

```python
import cv2
import numpy as np

# ❌ BAD: Not checking if image loaded
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Crashes if file doesn't exist!

# ✅ GOOD: Always validate
img = cv2.imread('image.jpg')
if img is None:
    raise FileNotFoundError("Image not found")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ❌ BAD: Using Python loops for pixel manipulation
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i, j] = img[i, j] * 0.5  # Extremely slow!

# ✅ GOOD: Vectorized NumPy operations
img = (img * 0.5).astype(np.uint8)

# ❌ BAD: Displaying BGR image with matplotlib
plt.imshow(img)  # Colors will be wrong!

# ✅ GOOD: Convert to RGB first
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)

# ❌ BAD: Not releasing video capture
cap = cv2.VideoCapture('video.mp4')
while cap.read()[0]:
    pass
# Memory leak! Camera still locked!

# ✅ GOOD: Always release
cap = cv2.VideoCapture('video.mp4')
try:
    while cap.read()[0]:
        pass
finally:
    cap.release()
```

## Image I/O and Display

### Reading and Writing Images

```python
import cv2

# Read image (returns None if failed)
img = cv2.imread('image.jpg')

# Read as grayscale
gray = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Read with alpha channel
img_alpha = cv2.imread('image.png', cv2.IMREAD_UNCHANGED)

# Write image
cv2.imwrite('output.jpg', img)

# Write with quality (JPEG: 0-100, PNG: 0-9 compression)
cv2.imwrite('output.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite('output.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

# Check if image loaded
if img is None:
    print("Error: Could not load image")
else:
    print(f"Image shape: {img.shape}")  # (height, width, channels)
```

### Display Images

```python
import cv2

# Display image in window
cv2.imshow('Window Name', img)
cv2.waitKey(0)  # Wait indefinitely for key press
cv2.destroyAllWindows()

# Display for specific duration (milliseconds)
cv2.imshow('Image', img)
cv2.waitKey(3000)  # Wait 3 seconds
cv2.destroyAllWindows()

# Display multiple images
cv2.imshow('Original', img)
cv2.imshow('Gray', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Display with matplotlib (convert BGR to RGB!)
import matplotlib.pyplot as plt

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis('off')
plt.show()
```

### Video Capture

```python
import cv2

# Open camera (0 = default, 1 = second camera, etc.)
cap = cv2.VideoCapture(0)

# Open video file
cap = cv2.VideoCapture('video.mp4')

# Check if opened successfully
if not cap.isOpened():
    print("Error: Could not open video")
    exit()

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video: {width}x{height} @ {fps} fps, {total_frames} frames")

# Read and process frames
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("End of video or error")
        break
    
    # Process frame here
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Writing Videos

```python
import cv2

cap = cv2.VideoCapture('input.mp4')

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID', 'MJPG'
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Process frame
    processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)  # Convert back to 3-channel
    
    # Write frame
    out.write(processed)

cap.release()
out.release()
cv2.destroyAllWindows()
```

## Image Transformations

### Resizing and Cropping

```python
import cv2

img = cv2.imread('image.jpg')

# Resize to specific dimensions
resized = cv2.resize(img, (800, 600))  # (width, height)

# Resize by scale factor
scaled = cv2.resize(img, None, fx=0.5, fy=0.5)  # 50% of original

# Resize with interpolation methods
resized_linear = cv2.resize(img, (800, 600), interpolation=cv2.INTER_LINEAR)  # Default
resized_cubic = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # Better quality
resized_area = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)  # Best for shrinking

# Crop (using NumPy slicing)
height, width = img.shape[:2]
cropped = img[100:400, 200:600]  # [y1:y2, x1:x2]

# Center crop
crop_size = 300
center_x, center_y = width // 2, height // 2
x1 = center_x - crop_size // 2
y1 = center_y - crop_size // 2
center_cropped = img[y1:y1+crop_size, x1:x1+crop_size]
```

### Rotation and Flipping

```python
import cv2

# Flip horizontally
flipped_h = cv2.flip(img, 1)

# Flip vertically
flipped_v = cv2.flip(img, 0)

# Flip both
flipped_both = cv2.flip(img, -1)

# Rotate 90 degrees clockwise
rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# Rotate 180 degrees
rotated_180 = cv2.rotate(img, cv2.ROTATE_180)

# Rotate 90 degrees counter-clockwise
rotated_90_ccw = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Rotate by arbitrary angle (around center)
height, width = img.shape[:2]
center = (width // 2, height // 2)
angle = 45  # degrees

# Get rotation matrix
M = cv2.getRotationMatrix2D(center, angle, scale=1.0)

# Apply rotation
rotated = cv2.warpAffine(img, M, (width, height))

# Rotate and scale
M_scaled = cv2.getRotationMatrix2D(center, 30, scale=0.8)
rotated_scaled = cv2.warpAffine(img, M_scaled, (width, height))
```

### Color Space Conversions

```python
import cv2

img = cv2.imread('image.jpg')

# BGR to RGB (for matplotlib)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR to HSV (useful for color-based segmentation)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# BGR to LAB
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Grayscale to BGR (add color channels)
gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# Extract individual channels
b, g, r = cv2.split(img)

# Merge channels
merged = cv2.merge([b, g, r])
```

## Image Filtering and Enhancement

### Blurring and Smoothing

```python
import cv2

# Gaussian blur (reduce noise)
blurred = cv2.GaussianBlur(img, (5, 5), 0)  # (kernel_size, sigma)

# Median blur (good for salt-and-pepper noise)
median = cv2.medianBlur(img, 5)  # kernel_size must be odd

# Bilateral filter (edge-preserving smoothing)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)  # (d, sigmaColor, sigmaSpace)

# Average blur
avg_blur = cv2.blur(img, (5, 5))

# Box filter
box = cv2.boxFilter(img, -1, (5, 5))
```

### Edge Detection

```python
import cv2

# Convert to grayscale first
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny edge detection
edges = cv2.Canny(gray, threshold1=50, threshold2=150)

# Sobel edge detection (gradient in x and y)
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # X gradient
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # Y gradient
sobel = cv2.magnitude(sobelx, sobely)

# Laplacian edge detection
laplacian = cv2.Laplacian(gray, cv2.CV_64F)

# Scharr (more accurate than Sobel for small kernels)
scharrx = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
scharry = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
```

### Morphological Operations

```python
import cv2
import numpy as np

# Define kernel
kernel = np.ones((5, 5), np.uint8)

# Erosion (shrink white regions)
eroded = cv2.erode(img, kernel, iterations=1)

# Dilation (expand white regions)
dilated = cv2.dilate(img, kernel, iterations=1)

# Opening (erosion followed by dilation) - removes noise
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Closing (dilation followed by erosion) - closes gaps
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# Gradient (difference between dilation and erosion) - outlines
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# Top hat (difference between input and opening) - bright spots
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# Black hat (difference between closing and input) - dark spots
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
```

### Thresholding

```python
import cv2

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Simple threshold
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Binary inverse
ret, thresh_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# Truncate
ret, thresh_trunc = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)

# To zero
ret, thresh_tozero = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)

# Otsu's thresholding (automatic threshold calculation)
ret, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptive thresholding (different threshold for different regions)
adaptive_mean = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
)

adaptive_gaussian = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)
```

## Contours and Shape Detection

### Finding and Drawing Contours

```python
import cv2

# Convert to grayscale and threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw all contours
img_contours = img.copy()
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)  # -1 = all contours

# Draw specific contour
cv2.drawContours(img_contours, contours, 0, (255, 0, 0), 3)  # First contour

# Iterate through contours
for i, contour in enumerate(contours):
    # Calculate area
    area = cv2.contourArea(contour)
    
    # Calculate perimeter
    perimeter = cv2.arcLength(contour, True)
    
    # Filter by area
    if area > 1000:
        cv2.drawContours(img_contours, [contour], -1, (0, 0, 255), 2)
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img_contours, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

### Shape Approximation

```python
import cv2

for contour in contours:
    # Approximate contour to polygon
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # Number of vertices
    n_vertices = len(approx)
    
    # Classify shape
    if n_vertices == 3:
        shape = "Triangle"
    elif n_vertices == 4:
        # Check if rectangle or square
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
    elif n_vertices > 4:
        shape = "Circle" if n_vertices > 10 else "Polygon"
    
    # Draw and label
    cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    x, y = approx[0][0]
    cv2.putText(img, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
```

### Contour Features

```python
import cv2
import numpy as np

for contour in contours:
    # Moments (for center of mass)
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)
    
    # Minimum enclosing circle
    (x, y), radius = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(img, center, radius, (0, 255, 0), 2)
    
    # Fit ellipse (requires at least 5 points)
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        cv2.ellipse(img, ellipse, (255, 0, 255), 2)
    
    # Convex hull
    hull = cv2.convexHull(contour)
    cv2.drawContours(img, [hull], -1, (0, 255, 255), 2)
    
    # Solidity (contour area / convex hull area)
    hull_area = cv2.contourArea(hull)
    contour_area = cv2.contourArea(contour)
    solidity = contour_area / hull_area if hull_area > 0 else 0
```

## Feature Detection and Matching

### ORB (Oriented FAST and Rotated BRIEF)

```python
import cv2

img1 = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('image2.jpg', cv2.IMREAD_GRAYSCALE)

# Create ORB detector
orb = cv2.ORB_create(nfeatures=1000)

# Detect keypoints and compute descriptors
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Draw keypoints
img1_kp = cv2.drawKeypoints(img1, kp1, None, color=(0, 255, 0))

# Match descriptors using BFMatcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Sort matches by distance (best first)
matches = sorted(matches, key=lambda x: x.distance)

# Draw top matches
img_matches = cv2.drawMatches(
    img1, kp1, img2, kp2, matches[:50],
    None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

cv2.imshow('Matches', img_matches)
cv2.waitKey(0)
```

### SIFT (Scale-Invariant Feature Transform)

```python
import cv2

# Note: SIFT is in opencv-contrib-python, not opencv-python

img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Create SIFT detector
sift = cv2.SIFT_create()

# Detect keypoints and compute descriptors
keypoints, descriptors = sift.detectAndCompute(img, None)

# Draw keypoints
img_kp = cv2.drawKeypoints(
    img, keypoints, None,
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

print(f"Number of keypoints: {len(keypoints)}")
```

### Feature Matching with FLANN

```python
import cv2
import numpy as np

# Detect features
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Lowe's ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

print(f"Good matches: {len(good_matches)}")

# Draw good matches
img_matches = cv2.drawMatches(
    img1, kp1, img2, kp2, good_matches, None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)
```

## Object Detection

### Haar Cascade (Face Detection)

```python
import cv2

# Load pre-trained Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

img = cv2.imread('people.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Detect eyes in face region
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

cv2.imshow('Faces', img)
cv2.waitKey(0)
```

### Template Matching

```python
import cv2

img = cv2.imread('image.jpg')
template = cv2.imread('template.jpg')

# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

h, w = template_gray.shape

# Template matching
result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# Find locations above threshold
threshold = 0.8
locations = np.where(result >= threshold)

# Draw rectangles
for pt in zip(*locations[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

cv2.imshow('Matches', img)
cv2.waitKey(0)
```

## Practical Workflows

### 1. Document Scanner (Perspective Transform)

```python
import cv2
import numpy as np

def order_points(pts):
    """Order points: top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-left
    rect[2] = pts[np.argmax(s)]  # Bottom-right
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Top-right
    rect[3] = pts[np.argmax(diff)]  # Bottom-left
    
    return rect

def four_point_transform(image, pts):
    """Apply perspective transform to get bird's eye view."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    # Compute width and height
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))
    
    # Destination points
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")
    
    # Perspective transform
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped

# Usage
img = cv2.imread('document.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Find document contour (assume largest quadrilateral)
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    
    if len(approx) == 4:
        pts = approx.reshape(4, 2)
        scanned = four_point_transform(img, pts)
        cv2.imshow('Scanned', scanned)
        cv2.waitKey(0)
        break
```

### 2. Motion Detection

```python
import cv2

def detect_motion(video_path):
    """Detect motion in video using frame differencing."""
    cap = cv2.VideoCapture(video_path)
    
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    while cap.isOpened():
        # Compute difference between frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        
        # Dilate to fill gaps
        dilated = cv2.dilate(thresh, None, iterations=3)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw bounding boxes
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Motion", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow('Motion Detection', frame1)
        
        # Update frames
        frame1 = frame2
        ret, frame2 = cap.read()
        
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Usage
# detect_motion('video.mp4')
```

### 3. Color-Based Object Tracking

```python
import cv2
import numpy as np

def track_colored_object(video_path, lower_color, upper_color):
    """Track object by color in HSV space."""
    cap = cv2.VideoCapture(video_path)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for color
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Remove noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find largest contour
            largest = max(contours, key=cv2.contourArea)
            
            # Get center and radius
            ((x, y), radius) = cv2.minEnclosingCircle(largest)
            
            if radius > 10:
                # Draw circle and center
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
        
        cv2.imshow('Tracking', frame)
        cv2.imshow('Mask', mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Usage: Track red object
# lower_red = np.array([0, 100, 100])
# upper_red = np.array([10, 255, 255])
# track_colored_object(0, lower_red, upper_red)
```

### 4. QR Code Detection

```python
import cv2

def detect_qr_code(image_path):
    """Detect and decode QR codes."""
    img = cv2.imread(image_path)
    
    # Initialize QR code detector
    detector = cv2.QRCodeDetector()
    
    # Detect and decode
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    
    if bbox is not None:
        # Draw bounding box
        n_lines = len(bbox)
        for i in range(n_lines):
            point1 = tuple(bbox[i][0].astype(int))
            point2 = tuple(bbox[(i+1) % n_lines][0].astype(int))
            cv2.line(img, point1, point2, (0, 255, 0), 3)
        
        # Display decoded data
        if data:
            print(f"QR Code data: {data}")
            cv2.putText(img, data, (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('QR Code', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Usage
# detect_qr_code('qrcode.jpg')
```

### 5. Image Stitching (Panorama)

```python
import cv2

def create_panorama(images):
    """Stitch multiple images into panorama."""
    # Create stitcher
    stitcher = cv2.Stitcher_create()
    
    # Stitch images
    status, pano = stitcher.stitch(images)
    
    if status == cv2.Stitcher_OK:
        print("Panorama created successfully")
        return pano
    else:
        print(f"Error: {status}")
        return None

# Usage
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')
img3 = cv2.imread('image3.jpg')

panorama = create_panorama([img1, img2, img3])

if panorama is not None:
    cv2.imshow('Panorama', panorama)
    cv2.waitKey(0)
```

## Performance Optimization

### Use GPU Acceleration

```python
import cv2

# Check CUDA availability
print(f"CUDA devices: {cv2.cuda.getCudaEnabledDeviceCount()}")

# Upload to GPU
gpu_img = cv2.cuda_GpuMat()
gpu_img.upload(img)

# GPU operations (must use cv2.cuda module)
gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)

# Download from GPU
result = gpu_gray.download()
```

### Vectorize Operations

```python
# ❌ SLOW: Python loops
for i in range(height):
    for j in range(width):
        img[i, j] = img[i, j] * 0.5

# ✅ FAST: NumPy vectorization
img = (img * 0.5).astype(np.uint8)

# ✅ FAST: OpenCV built-in functions
img = cv2.convertScaleAbs(img, alpha=0.5, beta=0)
```

### Multi-threading for Video

```python
import cv2
from threading import Thread
from queue import Queue

class VideoCapture:
    """Threaded video capture for better performance."""
    
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.q = Queue(maxsize=128)
        self.stopped = False
        
    def start(self):
        Thread(target=self._reader, daemon=True).start()
        return self
        
    def _reader(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if not ret:
                self.stop()
                break
            self.q.put(frame)
                
    def read(self):
        return self.q.get()
    
    def stop(self):
        self.stopped = True
        self.cap.release()

# Usage
cap = VideoCapture(0).start()
while True:
    frame = cap.read()
    # Process frame...
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.stop()
```

## Common Pitfalls and Solutions

### The "BGR vs RGB" Color Confusion

OpenCV uses BGR, most other libraries use RGB.

```python
# ❌ Problem: Colors look wrong in matplotlib
img = cv2.imread('image.jpg')
plt.imshow(img)  # Blue and red are swapped!

# ✅ Solution: Convert to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)

# ✅ Alternative: Use OpenCV's imshow
cv2.imshow('Correct Colors', img)
cv2.waitKey(0)
```

### The "Window Won't Close" Problem

Windows stay open without proper key handling.

```python
# ❌ Problem: Window frozen
cv2.imshow('Image', img)
# Program hangs!

# ✅ Solution: Always use waitKey
cv2.imshow('Image', img)
cv2.waitKey(0)  # Wait for key press
cv2.destroyAllWindows()
```

### The "Video Capture Not Released" Problem

Camera stays locked if not released properly.

```python
# ❌ Problem: Camera locked after crash
cap = cv2.VideoCapture(0)
# ... code crashes ...
# Camera still locked!

# ✅ Solution: Use try-finally
cap = cv2.VideoCapture(0)
try:
    while True:
        ret, frame = cap.read()
        # ... process ...
finally:
    cap.release()
    cv2.destroyAllWindows()
```

### The "Image Modification" Confusion

Some operations modify in-place, others return new images.

```python
# In-place modification
cv2.rectangle(img, (10, 10), (100, 100), (0, 255, 0), 2)  # Modifies img

# Returns new image
blurred = cv2.GaussianBlur(img, (5, 5), 0)  # img unchanged

# ✅ Always use .copy() if you need original
img_copy = img.copy()
cv2.rectangle(img_copy, (10, 10), (100, 100), (0, 255, 0), 2)
```

### The "Contour Hierarchy" Misunderstanding

`findContours` returns different structures based on retrieval mode.

```python
# External contours only (most common)
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# All contours with full hierarchy
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
)

# ⚠️ hierarchy structure: [Next, Previous, First_Child, Parent]
# Most use cases only need RETR_EXTERNAL
```

OpenCV is the Swiss Army knife of computer vision. Its vast library of optimized algorithms, combined with Python's ease of use, makes it the perfect tool for everything from simple image processing to complex real-time vision systems. Master these fundamentals, and you'll have the foundation to tackle any computer vision challenge.
