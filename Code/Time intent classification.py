import cv2
import os
import numpy as np
import time

# Set path to a directory of your 10 test images (PNG or JPG)
img_dir = "Code\Frames"
img_files = sorted([os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.endswith('.png') or f.endswith('.jpg')])

# Detailed (Canny + edge analysis)
detailed_times = []
for f in img_files[:len(img_files)]:
    start = time.time()
    img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (320, 240))
    edges = cv2.Canny(img, 60, 150)
    horiz_edges = np.sum(edges, axis=1)
    lower_half = horiz_edges[len(horiz_edges)//2:]
    _ = np.sum(lower_half > np.mean(lower_half) * 2.5)
    detailed_times.append(time.time() - start)
print("Detailed method avg time (10 frames):", sum(detailed_times)/len(img_files))

# Light (variance only)
light_times = []
for f in img_files[:len(img_files)]:
    start = time.time()
    img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (320, 240))
    lower_half = img[len(img)//2:, :]
    _ = np.var(lower_half)
    light_times.append(time.time() - start)
print("Light method avg time (10 frames):", sum(light_times)/len(img_files))