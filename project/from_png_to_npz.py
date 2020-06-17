#
#  Скрипт from_png_to_npz.py
#  Предназначен для упаковки массивов полученных из png-представлений 
#  Упакованные данные (датасет) используются при обучении  
#
#  Разработчик: Каневской Андрей
#  Таганрог 2020г
#

import numpy as np
import random
from PIL import Image
import project.project_const as P
import csv

# открывает изображение, конвертирует в черно-белое и возвращает массив
def getArrayFromImage(path):
  img = Image.open(path).convert('L')
  arr = np.array(img)[:, :, np.newaxis]
  return arr

# возвращает заглавную/прописную букву по коду
def getFinalCharacterNumber(number, mode):
  res = number
  if mode == 'l':
    res+=P.ALPHABET_SIZE
  return res

# список кодов шрифтов
fonts = []

# список режимов
# * u - upper - заглавные буквы
# * l - lower - прописные буквы
modes = ['u', 'l']

# загрузка шрифтов
with open('/home/andrew/Recognizerka/fonts/fonts/fonts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i>0 :
            fonts.append(row[0])
        i+=1

rotate_start = P.ROTATE_FROM
rotate_finish = P.ROTATE_TO
chars = P.ALPHABET_SIZE*2
fontsLen = len(fonts)
train_size = fontsLen*(rotate_finish-rotate_start+1)*chars

# упаковываем все изображения (тренировочные данные)
x_train = np.zeros((train_size, 32, 32, 1))
y_train = np.zeros((train_size, ))

n = 0
for font in fonts:
  print('** {0} **'.format(font))
  for mode in modes:
    for i in range(chars//2):
      for angle in range(rotate_start, rotate_finish+1):
        path = '{4}/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png'.format(font, mode, str(i), str(angle), P.P_DIR_PATH)
        x_train[n] = getArrayFromImage(path)
        y_train[n] = getFinalCharacterNumber(i, mode)
        n+=1

print('Summary train added: {0}'.format(n))

# упаковываем тестовые изображения (валидационные данные)
x_test = np.zeros((train_size//fontsLen, 32, 32, 1))
y_test = np.zeros((train_size//fontsLen, ))

n = 0
FONT=random.choice(fonts)
for mode in modes:
    for i in range(chars//2):
      for angle in range(rotate_start, rotate_finish+1):
        path = '{4}/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png'.format(FONT, mode, str(i), str(angle), P.P_DIR_PATH)
        x_test[n] = getArrayFromImage(path)
        y_test[n] = getFinalCharacterNumber(i, mode)
        n+=1

print('Summary test added: {0}'.format(n))

print(x_train.shape)
print(y_train.shape)

# сохраняем упакованные данные (формат numpy)
np.savez_compressed('{}/fonts/png32_rotated'.format(P.P_DIR_PATH), x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)
