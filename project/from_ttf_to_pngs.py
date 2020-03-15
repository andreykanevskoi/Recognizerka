import fontforge
import os

# path - path to foldet with ttf
# fontCode - name of ttf file
# lBegin - name of first russian lowercase character in ttf
# lEnd - name of last russian lowercase character in ttf
# uBegin - name of first russian uppercase character in ttf
# uEnd - name of last russian uppercase character in ttf
# lE - name of lower Er
# uE - name of upper Er


def unpackRussianPNGfromTTF(path, fontCode, fontType, lBegin, lEnd, uBegin, uEnd, lE, uE, size=32):
    newPath = path+"/pngs/"
    
    # make new directory
    # os.mkdir(newPath)

    # open font
    F = fontforge.open(path+"/"+fontCode+"."+fontType)


    # select uppercase chars
    temp = fontforge.font()
    F.selection.select(("ranges", None), uBegin, uEnd)
    F.copy()

    temp.selection.select(("ranges", None), "?", "^")
    temp.paste()

    # save uppercase chars
    i = 0
    for name in temp:
        PNGname = newPath+"{0}_u_{1}.png".format(fontCode, str(i))
        temp[name].export(PNGname, size-1)
        i += 1


    # select lowercase chars
    temp = fontforge.font()
    F.selection.select(("ranges", None), lBegin, lEnd)
    F.copy()

    temp.selection.select(("ranges", None), "?", "^")
    temp.paste()

    # save lowercase chars
    i = 0
    for name in temp:
        PNGname = newPath+"{0}_l_{1}.png".format(fontCode, str(i))
        temp[name].export(PNGname, size-1)
        i += 1

    # save Er
    i = 32
    
    temp = fontforge.font()
    F.selection.select(("ranges", None), lE, lE)
    F.copy()

    temp.selection.select(("ranges", None), "?", "?")
    temp.paste()

    for name in temp:
        PNGname = newPath+"{0}_l_{1}.png".format(fontCode, str(i))
        temp[name].export(PNGname, size-1)

    temp = fontforge.font()
    F.selection.select(("ranges", None), uE, uE)
    F.copy()

    temp.selection.select(("ranges", None), "?", "?")
    temp.paste()
    
    for name in temp:
        PNGname = newPath+"{0}_u_{1}.png".format(fontCode, str(i))
        temp[name].export(PNGname, size-1)

path = '/home/andrew/Recognizerka/fonts/fonts'

import csv

fontCodes = []
fontTypes = []
lowerBegins = []
lowerEnds = []
upperBegins = []
upperEnds = []
lEs = []
uEs = []

with open('/home/andrew/Recognizerka/fonts/fonts/fonts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i>0 :
            fontCodes.append(row[0])
            fontTypes.append(row[1])
            lowerBegins.append(row[2])
            lowerEnds.append(row[3])
            upperBegins.append(row[4])
            upperEnds.append(row[5])
            lEs.append(row[6])
            uEs.append(row[7])
        i+=1

fontsAmount = len(fontCodes)
for i in range(fontsAmount):
    unpackRussianPNGfromTTF(path, fontCodes[i], fontTypes[i], lowerBegins[i], lowerEnds[i], upperBegins[i], upperEnds[i], lEs[i], uEs[i], size=32)