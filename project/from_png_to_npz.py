import numpy as np
import random
from PIL import Image

def getArrayFromImage(path):
  img = Image.open(path).convert('L')
  arr = np.array(img).reshape(32,32,1)
  return arr

def getNullArrayExcept(number):
  arr = np.zeros((66))
  arr[number] = 1
  return arr

def getFinalCharacterNumber(number, mode):
  res = number
  if mode == 'l':
    res+=33
  return res

import csv

fonts = []
modes = ['u', 'l']

with open('/home/andrew/Recognizerka/fonts/fonts/fonts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i>0 :
            fonts.append(row[0])
        i+=1

rotate_start = -17
rotate_finish = 17
chars = 66
fontsLen = len(fonts)
train_size = fontsLen*(rotate_finish-rotate_start+1)*chars

# create train-set
x_train = np.zeros((train_size, 32, 32, 1))
y_train = np.zeros((train_size, ))

n = 0
for font in fonts:
  print('** {0} **'.format(font))
  for mode in modes:
    for i in range(chars//2):
      for angle in range(rotate_start, rotate_finish+1):
        path = '/home/andrew/Recognizerka/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png'.format(font, mode, str(i), str(angle))
        x_train[n] = getArrayFromImage(path)
        y_train[n] = getFinalCharacterNumber(i, mode)
        n+=1

print('Summary train added: {0}'.format(n))

# create test-set
x_test = np.zeros((train_size//fontsLen, 32, 32, 1))
y_test = np.zeros((train_size//fontsLen, ))

n = 0
FONT=random.choice(fonts)
for mode in modes:
    for i in range(chars//2):
      for angle in range(rotate_start, rotate_finish+1):
        path = '/home/andrew/Recognizerka/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png'.format(FONT, mode, str(i), str(angle))
        x_test[n] = getArrayFromImage(path)
        y_test[n] = getFinalCharacterNumber(i, mode)
        n+=1

print('Summary test added: {0}'.format(n))

np.savez_compressed('/home/andrew/Recognizerka/fonts/png32_rotated', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)