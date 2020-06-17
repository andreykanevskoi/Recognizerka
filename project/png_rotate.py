#
#  Скрипт png_rotate.py
#  Предназначен для обработки png-представлений символов шрифтов
#  Вращает изображение и сохраняет каждый поворот
#
#  Разработчик: Каневской Андрей
#  Таганрог 2020г
#

from PIL import Image
import csv
import project_const as P

ROTATE_FROM = -17
ROTATE_TO = 18

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
# 3. добавляется вращение от -17 до 17 градусов включительно
# 4. каждая версия поворота сохраняется в папку
for font in fonts:
  for mode in modes:
    for i in range(P.ALPHABET_SIZE):
      name = "{3}/fonts/fonts/pngs/{0}_{1}_{2}.png".format(font, mode, str(i), P.P_DIR_PATH)
      im = Image.open(name) # открывается изображение
      for angle in range(ROTATE_FROM, ROTATE_TO):
        im1 = im.rotate(angle) # поворот на angle градусов
        new_name = "{4}/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png".format(font, mode, str(i), str(angle), P.P_DIR_PATH)
        im1.save(new_name) # сохранение изображения
  
