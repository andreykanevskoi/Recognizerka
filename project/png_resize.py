#
#  Скрипт png_rotate.py
#  Предназначен для обработки png-представлений символов шрифтов
#  Приводит исходные png к формату 32x32
#
#  Разработчик: Каневской Андрей
#  Таганрог 2020г
#

from PIL import Image
import csv
import project_const as P

# список кодов шрифтов
fonts = []

# список режимов
# * u - upper - заглавные буквы
# * l - lower - прописные буквы
modes = ['u', 'l']

# из csv файла загружается список шрифтов
with open('{}/fonts/fonts/fonts.csv'.format(P.P_DIR_PATH)) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i>0 :
            fonts.append(row[0])
        i+=1

# 1. из каждого шрифта выбирается буква
# 2. загружается png-изображение буквы
# 3. размер приводится к 32х32
# 4. каждая версия сохраняется в папку
for font in fonts:
  for mode in modes:
    for i in range(33):
      name = "{3}/fonts/fonts/pngs/{0}_{1}_{2}.png".format(font, mode, str(i), P.P_DIR_PATH)
      im = Image.open(name)
      im = im.resize((32,32))
      im.save(name)
  
