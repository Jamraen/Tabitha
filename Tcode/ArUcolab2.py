import cv2
import numpy as np

DICT = cv2.aruco.DICT_4X4_50


def main():
    image_path = r"T:\testimages\aruco_test.jpg"

    loaded_image = cv2.imread(image_path)

    if loaded_image is None:
        print("Could not load image:", image_path)
        return

    dictionary = cv2.aruco.getPredefinedDictionary(DICT)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    corners_list, ids, rejected = detector.detectMarkers(loaded_image)

    print("IDs found:", ids)

    # Draw detected markers
    preview = loaded_image.copy()
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(preview, corners_list, ids)

    out_path = image_path.replace(".jpg", "_detected.jpg")
    cv2.imwrite(out_path, preview)

    print("Wrote preview:", out_path)


if __name__ == "__main__":
    main()