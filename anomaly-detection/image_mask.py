from __future__ import print_function
from PIL import Image,ImageDraw
import matplotlib.pyplot as plt


im = Image.open("NLM-MontgomeryCXRSet\\MontgomerySet\\CXR_png\\MCUCXR_0001_0.png").convert("RGBA")
leftMask = Image.open("NLM-MontgomeryCXRSet\\MontgomerySet\\ManualMask\\leftMask\\MCUCXR_0001_0.png").convert("L")
rightMask = Image.open("NLM-MontgomeryCXRSet\\MontgomerySet\\ManualMask\\rightMask\\MCUCXR_0001_0.png").convert("L")
           
background=Image.new('L', im.size, color=0)
background.paste(leftMask, (0, 0),leftMask)
background.paste(rightMask, (0, 0),rightMask)

background = background.convert("RGBA")

draw = ImageDraw.Draw(background)
pix = background.load()
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if pix[i,j][0] == 255:
            draw.point((i,j),(255,0,0,127))

im.paste(background,(0, 0), background)

plt.imshow(im)
plt.show()

