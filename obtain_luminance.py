"""
obtain_luminance.py

Francisco José Juan Quintanilla, Apr-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image
import sys

#Settings
img_path = "img/ref/lena.bmp" #Path of the img
header_path = "lena.h"
lines = 128 # How many lines are required to be extracted
###############################
#Start of the script
###############################

#Output file creating

f= open(header_path,"w+")

#Image opening and extracting
img = Image.open(img_path)
img = img.convert("YCbCr")
width, height = img.size
data = list(img.getdata())

#Correct input
if height < lines:
    print("WARN: Correcting variable lines as it is higher that the height of the image")
    lines = height

f.write("uint8_t img_data["+ str(width*lines)  + "] = {")

for index in range(0, width*lines):

    f.write(str(data[index][0]))
    if index != width*lines -1:
        f.write(", ")

f.write("};")

print("INFO: Written image",img_path, "into", header_path)