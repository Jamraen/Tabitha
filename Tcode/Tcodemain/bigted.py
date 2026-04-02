import cv2, os

import numpy as np


path = r"T:\Tcode\CameraTest\photos\ArucoTest\testphoto1_2026-03-08_16-54-24.jpg"

img = cv2.imread(path)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([15, 30, 30])

upper = np.array([45, 255, 255])

# lower = np.array([30, 100, 100])
#Unsuccessful values ^ and below
# upper = np.array([45, 255, 255])


mat_mask = cv2.inRange(hsv, lower, upper)

mask = cv2.bitwise_not(mat_mask)


# CLOSE = fill holes

k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_close, iterations=2)


# OPEN = remove specks

k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k_open, iterations=1)


base = os.path.splitext(path)[0]

cv2.imwrite(base + "_mask_clean.png", mask)


print("Wrote:", base + "_mask_clean.png")