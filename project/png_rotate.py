from PIL import Image
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


for font in fonts:
  for mode in modes:
    for i in range(33):
      name = "/home/andrew/Recognizerka/fonts/fonts/pngs/{0}_{1}_{2}.png".format(font, mode, str(i))
      im = Image.open(name)
      for angle in range(-17, 18):
        im1 = im.rotate(angle)
        new_name = "/home/andrew/Recognizerka/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png".format(font, mode, str(i), str(angle))
        im1.save(new_name)
  
