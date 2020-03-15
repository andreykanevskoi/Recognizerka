from PIL import Image

fonts = ['18847', '18872', '19046', '19051', '19081']
modes = ['u', 'l']

for font in fonts:
  for mode in modes:
    for i in range(33):
      name = "/home/andrew/Recognizerka/fonts/png_32_32/{0}_{1}_{2}.png".format(font, mode, str(i))
      im = Image.open(name)
      for angle in range(-13, 14):
        im1 = im.rotate(angle)
        new_name = "/home/andrew/Recognizerka/fonts/png_32_32_rotate/{0}_{1}_{2}_{3}.png".format(font, mode, str(i), str(angle))
        im1.save(new_name)
  
