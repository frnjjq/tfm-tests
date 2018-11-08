"""
random_loses.py

This script simulates what would happen in case of random looses of an 
image.Some scanlines are lost and those are interpolated later on using the 
ones rest in place.The interpolation to recover the image lost is bilinear.

To use modify the variables under settings:
looses      ->to configure the percentage of the image that is lost.
img_path    ->to indicate where to take the original image .
result_path ->to configure the path to leave the degradated image

PSNR function adapted from https://github.com/magonzalezc/PSNRtool.

Francisco José Juaan Quintanilla, Jan-2018
See LICENSE.md in the root of the repository
"""

import random
import math
from PIL import Image
from psnr import print_psnr

#Settings
looses = 0.8 #Percentage of line looses
img_path = "img/ref/lena.bmp" #Path of the img of line looses
result_path = "img/out/lena-random.bmp" #Path of the img of line looses
mode = 1

###############################
#Start of the script
###############################

print("Taking image from", img_path)
#Image opening and extracting
img = Image.open(img_path)
img = img.convert("YCbCr")
width, height = img.size
data = list(img.getdata())

#Generate the lost scanlines randomly
scanlines_lost = []
scalines_available = list(range(0, width))
for x in range(0, int(width*looses)):
    possition = random.randint(0, len(scalines_available)-1)
    scanlines_lost.append(scalines_available[possition])
    scalines_available.pop(possition)
print("There are", len(scanlines_lost), "scanlines that has been lost a total of", (len(scanlines_lost)/height)*100,"% hasbeen lost" )

scalines_available.sort()

for scanline in scanlines_lost:

    scalines_available.sort()

    #find the next top scanline which is not lost
    upper_lines = list(filter(lambda line: line > scanline , scalines_available))
    upper_lines.sort()
    if not upper_lines:
        top_scanline = 0
    else:
        top_scanline = upper_lines[0]-scanline

    #find the next bottom scanline which is not lost
    lower_lines = list(filter(lambda line: line < scanline , scalines_available))
    lower_lines.sort(reverse=True)
    if not lower_lines:
        bot_scanline = width
    else:
        bot_scanline = lower_lines[0]-scanline

    #interpolate the line using the top and bot scanlines

    for pix in range(int(width*scanline), int((width*scanline)+width)-1):
        newdata = [0, 0, 0]
        if top_scanline == 0:
            newdata[0] = data[pix+(width*(bot_scanline))][0]
            newdata[1] = data[pix+(width*(bot_scanline))][1]
            newdata[2] = data[pix+(width*(bot_scanline))][2]

        elif bot_scanline == width:
            newdata[0] = data[pix+(width*(top_scanline))][0]
            newdata[1] = data[pix+(width*(top_scanline))][1]
            newdata[2] = data[pix+(width*(top_scanline))][2]
        else:
            if mode == 0:
                newdata[0] = int((data[pix+width*top_scanline][0]*(-bot_scanline) + data[pix+width*bot_scanline][0]*top_scanline) / (top_scanline-bot_scanline))
                newdata[1] = int((data[pix+width*top_scanline][1]*(-bot_scanline) + data[pix+width*bot_scanline][1]*top_scanline) / (top_scanline-bot_scanline))
                newdata[2] = int((data[pix+width*top_scanline][2]*(-bot_scanline) + data[pix+width*bot_scanline][2]*top_scanline) / (top_scanline-bot_scanline))
            elif mode == 1:
                distance_horizontal = abs(data[pix+(width*top_scanline)][0] - data[pix+(width*bot_scanline)][0])
                distance_tilt_left = abs(data[pix+(width*top_scanline)+1][0] - data[pix+(width*bot_scanline)-1][0])
                distance_tilt_right = abs(data[pix+(width*top_scanline)-1][0] - data[pix+(width*bot_scanline)+1][0])

                if distance_tilt_left <= distance_horizontal and distance_horizontal <= distance_tilt_right:
                    newdata[0] = int((data[pix+(width*top_scanline)+1][0]*(-bot_scanline) + data[pix+(width*bot_scanline)-1][0]*top_scanline) / (top_scanline-bot_scanline))
                    newdata[1] = int((data[pix+(width*top_scanline)+1][1]*(-bot_scanline) + data[pix+(width*bot_scanline)-1][1]*top_scanline) / (top_scanline-bot_scanline))
                    newdata[2] = int((data[pix+(width*top_scanline)+1][2]*(-bot_scanline) + data[pix+(width*bot_scanline)-1][2]*top_scanline) / (top_scanline-bot_scanline))
                elif distance_tilt_right <= distance_horizontal and distance_horizontal <= distance_tilt_left:
                    newdata[0] = int((data[pix+(width*top_scanline)-1][0]*(-bot_scanline) + data[pix+(width*bot_scanline)+1][0]*top_scanline) / (top_scanline-bot_scanline))
                    newdata[1] = int((data[pix+(width*top_scanline)-1][1]*(-bot_scanline) + data[pix+(width*bot_scanline)+1][1]*top_scanline) / (top_scanline-bot_scanline))
                    newdata[2] = int((data[pix+(width*top_scanline)-1][2]*(-bot_scanline) + data[pix+(width*bot_scanline)+1][2]*top_scanline) / (top_scanline-bot_scanline))
                else:
                    newdata[0] = int((data[pix+(width*top_scanline)][0]*(-bot_scanline) + data[pix+(width*bot_scanline)][0]*top_scanline) / (top_scanline-bot_scanline))
                    newdata[1] = int((data[pix+(width*top_scanline)][1]*(-bot_scanline) + data[pix+(width*bot_scanline)][1]*top_scanline) / (top_scanline-bot_scanline))
                    newdata[2] = int((data[pix+(width*top_scanline)][2]*(-bot_scanline) + data[pix+(width*bot_scanline)][2]*top_scanline) / (top_scanline-bot_scanline)) 
        data[pix] = tuple(newdata)

#Save back to the file
res = Image.new(img.mode, img.size)
res.putdata(data)
res = res.convert("RGB")
print("Storing degradated image in", result_path)
res.save(result_path)
print_psnr(list(img.getdata()), data)
