import cv2

import os


DICT = cv2.aruco.DICT_4X4_50


def main():
    os.makedirs("t:/Tcode/arucolabstuff", exist_ok=True)


dictionary = cv2.aruco.getPredefinedDictionary(DICT)


marker_size_px = 600 # size of the saved image (pixels)


for marker_id in range(0, 1): # 0,1,2,3
    marker_image = cv2.aruco.generateImageMarker(dictionary, marker_id, marker_size_px)


filename = os.path.join("t:/Tcode/arucolabstuff", f"aruco_{marker_id}.png")

cv2.imwrite(filename, marker_image)

print("Saved:", filename)


if __name__ == "__main__":
    main()