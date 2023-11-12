import pyautogui
import numpy as np
import cv2
from PIL import Image

# Capture a screenshot
im = pyautogui.screenshot().convert('RGB')
# print(type(im))

im = np.array(im)
# print(type(im))

im = im[:, :, ::-1]

im = cv2.resize(im, (960, 540))

im = Image.fromarray(im)

print(im.size)

# Get the size (width and height) of the screenshot
# width, height = im.size

# Print the size
# print(f"Width: {width}, Height: {height}")