import numpy as np 
from PIL import Image

def getFlatArrayFromImage(path):
  img = Image.open(path).convert('L')
  arr = np.array(img)

  flat_arr = arr.ravel()
  return flat_arr

def getNullArrayExcept(number):
  arr = np.zeros((66))
  arr[number] = 1
  return arr

def getFinalCharacterNumber(number, mode):
  res = number
  if mode == 'l':
    res+=33
  return res

fonts = ['18847', '18872', '19046', '19051', '19081']
modes = ['u', 'l']
rotate_start = -13
rotate_finish = 13

# create train-set
x_train = np.zeros((8910, 1024))
y_train = np.zeros((8910, 66))

n = 0
for font in fonts:
  print('** {0} **'.format(font))
  for mode in modes:
    for i in range(33):
      for angle in range(rotate_start, rotate_finish+1):
        path = '/home/andrew/Recognizerka/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png'.format(font, mode, str(i), str(angle))
        x_train[n] = getFlatArrayFromImage(path)
        y_train[n] = getNullArrayExcept(getFinalCharacterNumber(i, mode))
        n+=1

print('Summary train added: {0}'.format(n))

# create test-set
x_test = np.zeros((1782, 1024))
y_test = np.zeros((1782, 66))

n = 0
FONT='18847'
for mode in modes:
    for i in range(33):
      for angle in range(rotate_start, rotate_finish+1):
        path = '/home/andrew/Recognizerka/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png'.format(FONT, mode, str(i), str(angle))
        x_test[n] = getFlatArrayFromImage(path)
        y_test[n] = getNullArrayExcept(getFinalCharacterNumber(i, mode))
        n+=1

print('Summary test added: {0}'.format(n))

np.savez_compressed('/home/andrew/Recognizerka/fonts/png32_rotated', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)