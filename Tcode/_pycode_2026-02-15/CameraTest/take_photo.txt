import os
import time
import cv2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def ensure_output_folder(folder_name: str = "photos") -> str:
    """Create an output folder next to this script if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def make_filename(prefix: str = "photo") -> str:
    """Create a timestamped filename like photo_2026-02-15_14-03-22.jpg."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}.jpg"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main() -> None:
    out_dir = ensure_output_folder("photos")

    # 0 is usually the onboard camera.
    # If you have multiple cameras, try 1, 2, etc.
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open camera.")
        print("Try closing Zoom/Teams, or change VideoCapture(0) to VideoCapture(1).")
        return

    print("Camera opened.")
    print("Press:")
    print(" SPACE to take photo")
    print(" Q to quit")

    while True:
        ok, frame = cap.read()

        if not ok:
            print("ERROR: Could not read a frame from the camera.")
            break

        cv2.imshow("Preview - press SPACE to capture, Q to quit", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):
            label = input("Type a label for this photo (e.g. dress_blue_001): ").strip()

            if not label:
                label = "photo"

            filename = make_filename(label)
            save_path = os.path.join(out_dir, filename)

            cv2.imwrite(save_path, frame)
            print(f"Saved: {save_path}")

        elif key == ord("q"):
            print("Quitting.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
