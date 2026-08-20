# from t010_meowth_photography import ensure_output_folder, make_filename, take_photo
# from t020_lilted_rectify_aruco import rectify_image
# from t030_bigted_mask import maskphoto
# from t040_snorlax_measure import  measureimage
import t050_kecleon_shopify
import t010_meowth_photography
import t020_lilted_rectify_aruco
import t030_bigted_mask
import t040_snorlax_measure
import t00_guzzlord_storage
import tabitha_gui
import time
import os
folder_path = "T:\\Tcode\\Tcodemain\\tflow"
out_folder_with_path = out_dir = t010_meowth_photography.ensure_output_folder("photo_output_folder")
while True:
    timestamp = time.strftime("%d_%H-%M-%S")
    meowth_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_rawphoto_meowth.jpg".replace("xxxx", timestamp)
    lilted_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_rectified_lilted.jpg".replace("xxxx", timestamp)
    t00_guzzlord_storage.PHOTOFILEPATH = lilted_filename_with_path
    bigted_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_masked_bigted.jpg".replace("xxxx", timestamp)
    snorlax_filename_with_path = "T:\\Tcode\\Tcodemain\\tflow\\photo_output_folder\\garment_xxxx_measured_snorlax.jpg".replace("xxxx", timestamp)
    print(meowth_filename_with_path + "\n" + lilted_filename_with_path + "\n" + bigted_filename_with_path + "\n" + snorlax_filename_with_path)
    # take_photo(out_folder_with_path)
    t010_meowth_photography.take_photo(meowth_filename_with_path)
    rectify_ok = t020_lilted_rectify_aruco.rectify_image(meowth_filename_with_path, lilted_filename_with_path)
    if not rectify_ok:
        print("Sropping: could not produce a rectified photo. Fix the issue anove the run again.")
        exit()
    t030_bigted_mask.maskphoto(lilted_filename_with_path, bigted_filename_with_path)
    t040_snorlax_measure.measureimage(bigted_filename_with_path)
    outcome = tabitha_gui.tabitha_gui(bigted_filename_with_path)
    if outcome != "scan_next":
        break