from PIL import Image

fonts = ['18847', '18872', '19046', '19051', '19081']
modes = ['u', 'l']

for font in fonts:
  for mode in modes:
    for i in range(33):
      name = "/home/andrew/Recognizerka/fonts/png_32_32/{0}_{1}_{2}.png".format(font, mode, str(i))
      im = Image.open(name)
      im = im.resize((32,32))
      im.save(name)
  
