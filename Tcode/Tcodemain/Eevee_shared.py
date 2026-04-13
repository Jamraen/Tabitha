#these are the common functions shared among the other sections of Tabitha code.
def zigzagbotleft(mask, toprow, botrow, leftcol, rightcol):
    print("XX", toprow, botrow, leftcol, rightcol)
    numcol = rightcol - leftcol - 1
    numrow = botrow - toprow - 1
    print("huasfhaj", numcol, numrow, botrow)
    for startpix in range (numrow, 0, -1):
        r = startpix
        c = leftcol
        while r > toprow and c<= numcol:
            if mask[r, c] >= 250:
                print("Found white bottom left ", r, c)
                return r, c
            else:
                print(r, c)
                r = r + 1
                c = c + 1



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