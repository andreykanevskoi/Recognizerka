#
#  Скрипт from_ttf_to_pngs.py
#  Предназначен для получения png-представлений кириллицы
#  Данные о конфигурации каждого шрифта берутся из csv файла
#
#  Разработчик: Каневской Андрей
#  Таганрог 2020г
#

import fontforge
import project.project_const as P
import os

# path - путь к папке с ttf
# fontCode - имя файла ttf
# lBegin - код первой русской прописной буквы в ttf
# lEnd - код последней русской прописной буквы в ttf
# uBegin - код первой русской заглавной буквы в ttf
# uEnd - код последней русской заглавной буквы в ttf
# lE - код прописной ё
# uE - код заглавной Ё


def unpackRussianPNGfromTTF(path, fontCode, fontType, lBegin, lEnd, uBegin, uEnd, lE, uE, size=32):
    newPath = path+"/pngs/"

    # открываем шрифт
    F = fontforge.open(path+"/"+fontCode+"."+fontType)


    # выбираем и сохраняем заглавные буквы
    temp = fontforge.font()
    F.selection.select(("ranges", None), uBegin, uEnd)
    F.copy()

    temp.selection.select(("ranges", None), "?", "^")
    temp.paste()

    i = 0
    for name in temp:
        PNGname = newPath+"{0}_u_{1}.png".format(fontCode, str(i))
        temp[name].export(PNGname, size-1)
        i += 1


    # выбираем и сохраняем прописные буквы
    temp = fontforge.font()
    F.selection.select(("ranges", None), lBegin, lEnd)
    F.copy()

    temp.selection.select(("ranges", None), "?", "^")
    temp.paste()

    i = 0
    for name in temp:
        PNGname = newPath+"{0}_l_{1}.png".format(fontCode, str(i))
        temp[name].export(PNGname, size-1)
        i += 1

    # сохраняем Ё
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

path = '{}/fonts/fonts'.format(P.P_DIR_PATH)

import csv

fontCodes = []
fontTypes = []
lowerBegins = []
lowerEnds = []
upperBegins = []
upperEnds = []
lEs = []
uEs = []

with open('{}/fonts/fonts/fonts.csv'.format(P.P_DIR_PATH)) as csv_file:
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