import cv2
import numpy as np
import math
#these are the common functions shared among the other sections of Tabitha code.
def zigzagbotleft(mask, toprow, botrow, leftcol, rightcol):
    print("toprow", toprow, "botrow",botrow, "leftcol",leftcol, "rightcol",rightcol)
    numcol = rightcol - 1
    numrow = botrow - 1
    botrow = botrow - 1
    rightcol = rightcol - 1
    print("numcol", numcol, "numrow",numrow, "botrow",botrow)
    for startpix in range (numrow, 0, -1):
        r = startpix
        c = leftcol
        # print(r,c)
        while r > toprow and c<= numcol and r <= botrow and c >= leftcol:
            if mask[r, c] >= 250:
                print("Found white bottom left ", r, c)
                return r, c
            else:
                # print(r, c)
                mask[r, c] = 150
                r = r + 1
                c = c + 1
def measurepointsinpix(topleftrow, topleftcol, toprightrow, toprightcol, botrightrow, botrightcol, botleftrow, botleftcol):
    triangleopposite = abs(botleftrow - botrightrow)
    triangleadjacent = abs (botleftcol - botrightcol)
    trianglehyp = (triangleopposite**2 + triangleadjacent**2)**.5
    return trianglehyp

def zigzagbotright(mask, toprow, botrow, leftcol, rightcol):
    print("toprow", toprow, "botrow",botrow, "leftcol",leftcol, "rightcol",rightcol)
    numcol = rightcol - 1
    numrow = botrow - 1
    botrow = botrow - 1
    rightcol = rightcol - 1
    print("numcol", numcol, "numrow",numrow, "botrow",botrow)
    for startpix in range (numrow, 0, -1):
        r = startpix
        c = rightcol
        # print(r,c)
        while r > toprow and c<= numcol and r <= botrow and c >= leftcol:
            if mask[r, c] >= 250:
                print("Found white bottom right ", r, c)
                return r, c
            else:
                # print(r, c)
                mask[r, c] = 150
                r = r + 1
                c = c - 1

def zigzagtopleft(mask, toprow, botrow, leftcol, rightcol):
    print("toprow", toprow, "botrow",botrow, "leftcol",leftcol, "rightcol",rightcol)
    numcol = rightcol - 1
    numrow = botrow - 1
    botrow = botrow - 1
    rightcol = rightcol - 1
    print("numcol", numcol, "numrow",numrow, "botrow",botrow)
    for startpix in range (toprow, numrow, 1):
        r = startpix
        c = leftcol
        # print(r, c)
        while r > toprow and c<= numcol and r <= botrow and c >= leftcol:
            if mask[r, c] >= 250:
                print("Found white top left ", r, c)
                return r, c
            else:
                mask[r, c] = 150
                r = r - 1
                c = c + 1

def zigzagtopright(mask, toprow, botrow, leftcol, rightcol):
    print("toprow", toprow, "botrow",botrow, "leftcol",leftcol, "rightcol",rightcol)
    numcol = rightcol - 1
    numrow = botrow - 1
    botrow = botrow - 1
    rightcol = rightcol - 1
    print("numcol", numcol, "numrow",numrow, "botrow",botrow)
    for startpix in range (toprow, numrow , 1):
        r = startpix
        c = rightcol
        # print(r,c)
        while r > toprow and c<= numcol and r <= botrow and c >= leftcol:
            if mask[r, c] >= 250:
                print("Found white top right ", r, c)
                return r, c
            else:
                mask[r, c] = 150
                # print(r, c)
                r = r - 1
                c = c - 1

def makemaskpoint(mask, r, c, toprow, botrow, leftcol, rightcol):
    pointsize = 50
    half = pointsize // 2
    for row in range(r - half, r + half):
        for col in range(c - half, c + half):
            if toprow <= row < botrow and leftcol <= col < rightcol:
                mask[row, col] = 100
    return mask

def showmaskimage(mask, title="rename this window"):
    resized = cv2.resize(mask, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow(title, resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def removearucomask(mask, toprow, botrow, leftcol, rightcol):
    arucosize = 110
    botrow = botrow -1
    rightcol = rightcol - 1
    #Below is top left
    for row in range (0, arucosize, 1):
        for col in range (0, arucosize, 1):
            if mask[row, col] >= 250:
                mask[row, col] = 0
    #Above is top left
    #Below is bot left
    for row in range (botrow, botrow -arucosize, -1):
        for col in range (0, arucosize, 1):
            if mask[row, col] >= 250:
                mask[row, col] = 0
    #Above is bot left
    #Below it top right
    for row in range (0, arucosize, 1):
        for col in range (rightcol, rightcol - arucosize, -1):
            if mask[row, col] >= 250:
                mask[row, col] = 0
    #Above it top right
    #Below is bottom right
    for row in range (botrow, botrow - arucosize, -1):
        for col in range (rightcol, rightcol - arucosize, -1):
            if mask[row, col] >= 250:
                mask[row, col] = 0
    #above is bottom right.
    return mask

# print(numrow)
# print(numcol)
# colorpixel = mask[500, 500] 
# #This grabs the top left point on a garment.
# for currentrow in range (100, numrow-100, 1):
#     for currentcol in range (100, numcol-100, 1):
#         currentcolour = mask[currentrow, currentcol]   
#         if currentcolour == 255:
#             topwhite = currentrow
#             print(topwhite, currentcolour)
#             stopnowbool = True
#             break
#     if stopnowbool == True:
#             break
    
# stopnowbool = False

# for currentrow in range (numrow-100, 100, -1):
#     for currentcol in range (numcol-100, 100, -1):
#         currentcolour = mask[currentrow, currentcol]
#         # find corners of garment
#         if currentcolour == 255:
#             bottomwhite = currentrow
#             print(bottomwhite, currentcolour)
#             stopnowbool = True
#             break
#     if stopnowbool == True:
#             break

# heightinpixels = bottomwhite - topwhite
# heightincm = heightinpixels/30
# print(heightincm)