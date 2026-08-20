import os
import time
import subprocess
import t00_guzzlord_storage

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ensure_output_folder(folder_name: str = "photos") -> str:
    """Create an output folder next to this script if it doesn't exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def make_short_filename(prefix: str = "photo") -> str:
    """Create a timestamped filename like photo_2026-02-15_14-03-22.jpg."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}.jpg"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def make_filename(prefix: str = "photo", description: str = "descr", madeby: str = "creatingfile") -> str:
    """Create a timestamped filename like photo_2026-02-15_14-03-22.jpg."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    return f"{prefix}_{description}_{madeby}_{timestamp}.jpg"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

def take_photo(outfile) -> None:
    print("Taking photo...")
    subprocess.run(
        ["rpicam-still", "-o", outfile, "-n", "-t", "1"],
        check = True
    )
    print(f"Saved: {outfile}")

if __name__ == "__main__":
    take_photo()
