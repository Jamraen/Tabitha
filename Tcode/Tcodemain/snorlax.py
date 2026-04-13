import cv2
import numpy as np
import math
from .Eevee_shared import zigzagbotleft 
# photo height = 1140, photo width = 1035
# pixels per cm = 1140/38 = 30 for height and 1035/34.5 = 30
# MAT_W_CM = 34.5 MAT_H_CM = 38.0 these are the numbers from the rectification
mask = cv2.imread(
    "C:/Users/Jasmi/Downloads/Tabitha CDT/Tcode/Tcodemain/picnicbasket/shortsongreen_rectified_mask_clean.png",
    cv2.IMREAD_GRAYSCALE
)

color_img = cv2.imread(
    "C:/Users/Jasmi/Downloads/Tabitha CDT/Tcode/Tcodemain/picnicbasket/shortsongreen_rectified_mask_clean.png"
)
if color_img is None:
    print("ERROR: Could not load color image. Check file path.")
    exit()

# Ensure same size
color_img = cv2.resize(color_img, (mask.shape[1], mask.shape[0]))

mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
colored_masked = cv2.bitwise_and(color_img, mask_3ch)

cv2.imshow("Colored Masked", colored_masked)
cv2.waitKey(0)
cv2.destroyAllWindows()
# print(mask.shape)
stopnowbool = False
pixelspercm = 30
numrow = mask.shape[0]
numcol = mask.shape[1]
zigzagbotleft(toprow, botrow, leftcol, rightcol, mask)
print(numrow)
print(numcol)
colorpixel = mask[500, 500] 
#This grabs the top left point on a garment.
for currentrow in range (100, numrow-100, 1):
    for currentcol in range (100, numcol-100, 1):
        currentcolour = mask[currentrow, currentcol]   
        if currentcolour == 255:
            topwhite = currentrow
            print(topwhite, currentcolour)
            stopnowbool = True
            break
    if stopnowbool == True:
            break
    
stopnowbool = False

for currentrow in range (numrow-100, 100, -1):
    for currentcol in range (numcol-100, 100, -1):
        currentcolour = mask[currentrow, currentcol]
        # find corners of garment
        if currentcolour == 255:
            bottomwhite = currentrow
            print(bottomwhite, currentcolour)
            stopnowbool = True
            break
    if stopnowbool == True:
            break

heightinpixels = bottomwhite - topwhite
heightincm = heightinpixels/30
print(heightincm)