from t010_meowth_photography import ensure_output_folder, make_filename, take_photo
from t020_lilted_rectify_aruco import rectify_image
from t030_bigted_mask import maskphoto
from t040_snorlax_measure import  measureimage
import time
folder_path = "T:\\Tcode\\Tcodemain\\tflow"
out_folder_with_path = out_dir = ensure_output_folder("photo_output_folder")
timestamp = time.strftime("%d_%H-%M-%S")
meowth_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_rawphoto_meowth.jpg".replace("xxxx", timestamp)
lilted_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_rectified_lilted.jpg".replace("xxxx", timestamp)
bigted_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_masked_bigted.jpg".replace("xxxx", timestamp)
snorlax_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_measured_snorlax.jpg".replace("xxxx", timestamp)
print(meowth_filename_with_path + "\n" + lilted_filename_with_path + "\n" + bigted_filename_with_path + "\n" + snorlax_filename_with_path)
# take_photo(out_folder_with_path)
take_photo(meowth_filename_with_path)
filename = meowth_filename_with_path
meowth_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\testphoto.jpg"
rectify_image(meowth_filename_with_path, lilted_filename_with_path)
maskphoto(lilted_filename_with_path, bigted_filename_with_path)
measureimage(bigted_filename_with_path)