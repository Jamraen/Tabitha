import cv2
import numpy as np
import math
from t000_eevee_shared import zigzagbotleft
from t000_eevee_shared import zigzagtopleft
from t000_eevee_shared import zigzagtopright
from t000_eevee_shared import zigzagbotright
from t000_eevee_shared import removearucomask
from t000_eevee_shared import showmaskimage
from t000_eevee_shared import makemaskpoint
from t000_eevee_shared import measurepointsonskirt
# from t0_ketchum_main import bigted_filename_with_path
# photo height = 1140, photo width = 1035
# pixels per cm = 1140/38 = 30 for height and 1035/34.5 = 30
# MAT_W_CM = 34.5 MAT_H_CM = 38.0 these are the numbers from the rectification
# Ensure same size
matwidthincm = 34.5
matwidthinpix = 1035

# def convpixtocm():

def measureimage(bigted_filename_with_path):
    garment_type_number = "xs"
    while garment_type_number not in {"1", "2", "3", "4"}:
        garment_type_number = input("Please type 1 for skirt, 2 for dress, 3 for pants, 4 for shirt, then press enter: ")
        if garment_type_number == "1":
            garment_type = "skirt"
        elif garment_type_number == "2":
            garment_type = "dress"
        elif garment_type_number == "3":
            garment_type = "pants"
        elif garment_type_number == "4":
            garment_type = "shirt"
        else:
            print("You must enter a valid garment type" + str(garment_type_number))

    mask = cv2.imread(
        bigted_filename_with_path,
        cv2.IMREAD_GRAYSCALE
       )

    color_img = cv2.imread(
        bigted_filename_with_path
        )
    if color_img is None:
        print("ERROR: Could not load color image. Check file path.")
        exit()


    color_img = cv2.resize(color_img, (mask.shape[1], mask.shape[0]))
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    colored_masked = cv2.bitwise_and(color_img, mask_3ch)
    # cv2.imshow("Colored Masked", colored_masked)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(mask.shape)
    stopnowbool = False
    pixelspercm = 30
    numrow = mask.shape[0]
    numcol = mask.shape[1]
    toprow = 0
    botrow = mask.shape[0]
    leftcol = 0
    rightcol = mask.shape[1]
    print(toprow, botrow, leftcol, rightcol)
    arucoremove = removearucomask(mask, toprow, botrow, leftcol, rightcol)
    showimagemask = showmaskimage(mask, title="rename this window")
    botleftpoint = zigzagbotleft(mask, toprow, botrow, leftcol, rightcol)
    botleftrow = botleftpoint[0]
    botleftcol = botleftpoint[1]
    botrightpoint = zigzagbotright(mask, toprow, botrow, leftcol, rightcol)
    botrightrow = botrightpoint[0]
    botrightcol = botrightpoint[1]
    topleftpoint = zigzagtopleft(mask, toprow, botrow, leftcol, rightcol)
    topleftrow = topleftpoint[0]
    topleftcol = topleftpoint[1]
    toprightpoint = zigzagtopright(mask, toprow, botrow, leftcol, rightcol)
    toprightrow = toprightpoint[0]
    toprightcol = toprightpoint[1]
    mask = makemaskpoint(mask, botleftrow, botleftcol, toprow, botrow, leftcol, rightcol)
    mask = makemaskpoint(mask, botrightrow, botrightcol, toprow, botrow, leftcol, rightcol)
    mask = makemaskpoint(mask, topleftrow, topleftcol, toprow, botrow, leftcol, rightcol)
    mask = makemaskpoint(mask, toprightrow, toprightcol, toprow, botrow, leftcol, rightcol)
    showimagemask = showmaskimage(mask, title="rename this window")
    if garment_type == "skirt":
        measurementhemskirt = measurepointsonskirt(topleftrow, topleftcol, toprightrow, toprightcol, botrightrow, botrightcol, botleftrow, botleftcol)
        print(measurementhemskirt)


if __name__ == "__main__":
    measureimage()