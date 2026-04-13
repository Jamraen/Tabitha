#these are the common functions shared among the other sections of Tabitha code.
def zigzagbotleft(toprow, botrow, leftcol, rightcol, mask):
    numcol = rightcol - leftcol
    numrow = botrow - toprow
    for startpix in range (numrow, 0, -1):
        r = startpix
        c = leftcol
        while r > toprow and c<= numcol:
            if mask[r, c] >= 250:
                print("Found white bottom left ", r, c)
                return r, c
            else:
                r = r + 1
                c = c + 1