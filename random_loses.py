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

#Settings
looses = 0.5 #Percentage of line looses
img_path = "img/ref/lena.bmp" #Path of the img of line looses
result_path = "img/out/lena-random.bmp" #Path of the img of line looses

def print_psnr(original_data, degradated_data):
    """
    This calculates the Peak Signal to Noise Ratio (PSNR).
    :param original_data: As Pillow gives it with getdata
    :param degradated_data: As Pillow gives it with getdata
    :return:
    """
    error_y = 0
    error_cb = 0
    error_cr = 0

    for i in range(0, len(original_data)):
        dif_y = abs(original_data[i][0] - degradated_data[i][0])
        dif_cb = abs(original_data[i][1] - degradated_data[i][1])
        dif_cr = abs(original_data[i][2] - degradated_data[i][2])
        error_y += dif_y * dif_y
        error_cb += dif_cb * dif_cb
        error_cr += dif_cr * dif_cr

    mse_y = error_y / len(original_data)
    mse_cb = error_cb / len(original_data)
    mse_cr = error_cr / len(original_data)

    if mse_y != 0:
        psnr_y = float(-10.0 * math.log(mse_y / (255 * 255), 10))
    else:
        psnr_y = 0

    if mse_cb != 0:
        psnr_cb = float(-10.0 * math.log(mse_cb / (255 * 255), 10))
    else:
        psnr_cb = 0

    if mse_cr != 0:
        psnr_cr = float(-10.0 * math.log(mse_cr / (255 * 255), 10))
    else:
        psnr_cr = 0

    print('Y =', psnr_y, 'Cb =', psnr_cb, 'Cr =', psnr_cr)

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
print("There are", len(scanlines_lost), "scanlines that has been lost")

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

    for pix in range(int(width*scanline), int((width*scanline)+width)):
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
            newdata[0] = int((data[pix+(width*(top_scanline))][0]*(-bot_scanline) + data[pix+(width*(bot_scanline))][0]*top_scanline) / (top_scanline-bot_scanline))
            newdata[1] = int((data[pix+(width*(top_scanline))][1]*(-bot_scanline) + data[pix+(width*(bot_scanline))][1]*top_scanline) / (top_scanline-bot_scanline))
            newdata[2] = int((data[pix+(width*(top_scanline))][2]*(-bot_scanline) + data[pix+(width*(bot_scanline))][2]*top_scanline) / (top_scanline-bot_scanline))      
        data[pix] = tuple(newdata)

#Save back to the file
res = Image.new(img.mode, img.size)
res.putdata(data)
res = res.convert("RGB")
print("Storing degradated image in", result_path)
res.save(result_path)
print_psnr(list(img.getdata()), data)
