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

    corners_list, ids, _ = detector.detectMarkers(loaded_image)

    if ids is None:
        print("No markers found.")
        return

    ids = ids.flatten()

    for corners, marker_id in zip(corners_list, ids):
        pts = corners.reshape(4, 2).astype(np.float32)
        center = pts.mean(axis=0)

        print("Marker ID:", int(marker_id))
        print("Corners:\n", pts)
        print("Center:", center)
        print("-" * 40)


if __name__ == "__main__":
    main()