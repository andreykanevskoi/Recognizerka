
import fontforge
fontname = "19081"
F = fontforge.open("/home/andrew/Recognizerka/fonts/"+fontname+".ttf")

F.selection.select(("ranges",None), "uni0451","uni0451")
F.copy()

upper=fontforge.font()
upper.selection.select(("ranges",None),"?","?")
upper.paste()

i = 32
mode = "l"
for name in upper:
  filename = "/home/andrew/Recognizerka/fonts/{0}/{0}_{1}_{2}.png".format(fontname, mode, str(i))
  print (name)
  upper[name].export(filename, 32)
  i+=1

# F.selection.select(("ranges",None),"a","z")
# F.copy()

# lower=fontforge.font()
# lower.selection.select(("ranges",None),"a","z")
# lower.paste()

# for name in lower:
#   filename = "/home/andrew/Recognizerka/fonts/"+fontname+"/" + name + ".png"
#   print (name)
#   lower[name].export(filename, 32)
