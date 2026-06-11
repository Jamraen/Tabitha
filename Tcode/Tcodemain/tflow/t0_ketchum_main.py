from t010_meowth_photography import ensure_output_folder, make_filename, take_photo
from t020_lilted_rectify_aruco import rectify_image
import time
folder_path = "T:\\Tcode\\Tcodemain\\tflow"
out_folder_with_path = out_dir = ensure_output_folder("photo_output_folder")
timestamp = time.strftime("%d_%H-%M-%S")
#Generate all the required filenames
# call this to make the filename def make_filename(prefix: str = "photo", description: str = "descr", madeby: str = "creatingfile") -> str:
rawfilename = make_filename("garment", "", timestamp)

# take_photo(out_folder_with_path)
filename = "testphoto"
rectify_image(out_folder_with_path, filename)