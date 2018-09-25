"""
obtain_luminance.py

Francisco José Juan Quintanilla, Apr-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image

#Settings
img_path = "img/ref/lena.bmp" #Path of the img

###############################
#Start of the script
###############################


#Image opening and extracting
img = Image.open(img_path)
img = img.convert("YCbCr")
width, height = img.size
data = list(img.getdata())

print("uint8_t lena[",width*height, "] = {", end='', flush=True)

for pix in data:
    print(pix[0], ",", end='', flush=True)

print("};", end='', flush=True)

