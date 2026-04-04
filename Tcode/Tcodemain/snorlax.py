import cv2
import numpy as np
import math
# photo height = 1140, photo width = 1035
# pixels per cm = 1140/38 = 30 for height and 1035/34.5 = 30
# MAT_W_CM = 34.5 MAT_H_CM = 38.0 these are the numbers from the rectification
mask = cv2.imread ("C:/Users/Jasmi/Downloads/Tabitha CDT/Tcode/Tcodemain/picnicbasket/shortsongreen_rectified_mask_clean.png", cv2.IMREAD_GRAYSCALE)
# print(mask.shape)
stopnowbool = False
pixelspercm = 30
numrow = mask.shape[0]
numcol = mask.shape[1]
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