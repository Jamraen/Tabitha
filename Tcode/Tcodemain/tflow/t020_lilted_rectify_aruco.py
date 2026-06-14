##Currently working, just had to input the correct photo location
import cv2
import numpy as np
import t00_guzzlord_storage

DICT = cv2.aruco.DICT_4X4_50

# MAT_W_CM = 34.5
# MAT_H_CM = 60


CORNER_IDS = {0: "TL", 1: "TR", 2: "BR", 3: "BL"}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def detect_aruco_corners(loaded_image: np.ndarray) -> dict[int, np.ndarray]:
    dictionary = cv2.aruco.getPredefinedDictionary(DICT)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    corners_list, ids, _ = detector.detectMarkers(loaded_image)

    if ids is None:
        return {}

    ids = ids.flatten()
    found = {}

    for corners, marker_id in zip(corners_list, ids):
        marker_id = int(marker_id)

        if marker_id in CORNER_IDS:
            pts = corners.reshape(4, 2).astype(np.float32)
            center = pts.mean(axis=0)
            found[marker_id] = center

    return found
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rectify_to_mat(loaded_image: np.ndarray):
    found = detect_aruco_corners(loaded_image)

    missing = [mid for mid in CORNER_IDS if mid not in found]
    if missing:
        raise ValueError(f"Missing ArUco corner IDs in image: {missing}")

    # source points in the original photo
    src = np.array(
        [found[0], found[1], found[2], found[3]],
        dtype=np.float32
    )

    # output size
    W = int(round(t00_guzzlord_storage.MAT_W_CM * t00_guzzlord_storage.PIXELS_PER_CM))
    H = int(round(t00_guzzlord_storage.MAT_H_CM * t00_guzzlord_storage.PIXELS_PER_CM))

    # destination rectangle
    dst = np.array(
        [[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]],
        dtype=np.float32
    )

    # perspective transform
    Hmat = cv2.getPerspectiveTransform(src, dst)

    # warp image
    rectified = cv2.warpPerspective(
        loaded_image, Hmat, (W, H), flags=cv2.INTER_LINEAR
    )

    return rectified, Hmat
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rectify_image(meowth_filename_with_path, lilted_filename_with_path):

    # image_path = r"T:\Tcode\Tcodemain\picnicbasket\Shortsongreen.jpg"
    # img_file_with_path = image_path + "\\" + filename
    # print("THE IMAGE", img_file_with_path)
    # loaded_image = cv2.imread(image_path)
    print("GOT TO HERE", meowth_filename_with_path)
    loaded_image = cv2.imread(meowth_filename_with_path)
    t00_guzzlord_storage.MAT_W_PIX = loaded_image.shape[1]
    t00_guzzlord_storage.PIXELS_PER_CM = round(t00_guzzlord_storage.MAT_W_PIX / t00_guzzlord_storage.MAT_W_CM)
    print(t00_guzzlord_storage.PIXELS_PER_CM)
    if loaded_image is None:
        print("Could not load image:", meowth_filename_with_path)
        return

    try:
        rectified, _ = rectify_to_mat(loaded_image)
    except ValueError as e:
        print(e)
        return

    out_path = lilted_filename_with_path
    cv2.imwrite(out_path, rectified)

    print("Wrote:", out_path)
    print("pixels_per_cm used:", t00_guzzlord_storage.PIXELS_PER_CM)
    print("Rectified size (pixels):", rectified.shape[1], "x", rectified.shape[0])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    rectify_image()