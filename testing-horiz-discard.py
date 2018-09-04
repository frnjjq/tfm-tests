"""
testing-horiz-discard.py

Testing for horizontal interpolation of lost scanlines.

Francisco José Juaan Quintanilla, Jul-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image
from psnr import print_psnr

#Settings
lines_lost = 2 #Distance between preserved scalines
img_path = "img/ref/lena_128.bmp" #Path of the img of line looses
result_path = "img/out/lena_128_2.png" #Path of the img of line looses
mode = 2 # 

###############################
#Start of the script
###############################

print("Taking image from", img_path)

#Image opening and extracting
img = Image.open(img_path)
img = img.convert("YCbCr")
width, height = img.size
data = list(img.getdata())

for line in range(height - (height-1)%lines_lost):
    prev_line = line % lines_lost
    next_line = lines_lost - prev_line

    if prev_line != 0: # If the line is not preserved and shoukd be reconstructed

        if mode == 0:
            for pix in range(width*line, width*line + width):
                newdata = [0, 0, 0]
                newdata[0] = int((data[pix+(width*next_line)][0]*prev_line + data[pix-(width*prev_line)][0]*next_line) / lines_lost)
                newdata[1] = int((data[pix+(width*next_line)][1]*prev_line + data[pix-(width*prev_line)][1]*next_line) / lines_lost)
                newdata[2] = int((data[pix+(width*next_line)][2]*prev_line + data[pix-(width*prev_line)][2]*next_line) / lines_lost)      
                data[pix] = tuple(newdata)
        elif mode == 1:
            for pix in range(width*line +1, width*line + width -1):
                newdata = [0, 0, 0]
                distance_horizontal = abs(data[pix+(width*next_line)][0] - data[pix-(width*prev_line)][0])
                distance_tilt_left = abs(data[pix+(width*next_line)+1][0] - data[pix-(width*prev_line)-1][0])
                distance_tilt_right = abs(data[pix+(width*next_line)-1][0] - data[pix-(width*prev_line)+1][0])

                if distance_tilt_left <= distance_horizontal and distance_horizontal <= distance_tilt_right:
                    newdata[0] = int((data[pix+(width*next_line)+1][0]*prev_line + data[pix-(width*prev_line)-1][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)+1][1]*prev_line + data[pix-(width*prev_line)-1][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)+1][2]*prev_line + data[pix-(width*prev_line)-1][2]*next_line) / lines_lost)
                elif distance_tilt_right <= distance_horizontal and distance_horizontal <= distance_tilt_left:
                    newdata[0] = int((data[pix+(width*next_line)-1][0]*prev_line + data[pix-(width*prev_line)+1][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)-1][1]*prev_line + data[pix-(width*prev_line)+1][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)-1][2]*prev_line + data[pix-(width*prev_line)+1][2]*next_line) / lines_lost)            
                else:
                    newdata[0] = int((data[pix+(width*next_line)][0]*prev_line + data[pix-(width*prev_line)][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)][1]*prev_line + data[pix-(width*prev_line)][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)][2]*prev_line + data[pix-(width*prev_line)][2]*next_line) / lines_lost)      
                data[pix] = tuple(newdata)
        elif mode == 2:
            for pix in range(width*line +1, width*line + width -1):
                newdata = [0, 0, 0]
                distance_horizontal = abs(data[pix+(width*next_line)][0] - data[pix-(width*prev_line)][0])
                distance_tilt_left = abs(data[pix+(width*next_line)+1][0] - data[pix-(width*prev_line)-1][0])
                distance_tilt_right = abs(data[pix+(width*next_line)-1][0] - data[pix-(width*prev_line)+1][0])

                if distance_horizontal <= distance_tilt_left*2 and distance_horizontal <= distance_tilt_right*2:
                    newdata[0] = int((data[pix+(width*next_line)][0]*prev_line + data[pix-(width*prev_line)][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)][1]*prev_line + data[pix-(width*prev_line)][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)][2]*prev_line + data[pix-(width*prev_line)][2]*next_line) / lines_lost)              
                elif distance_tilt_left <= distance_horizontal and distance_horizontal <= distance_tilt_right:
                    newdata[0] = int((data[pix+(width*next_line)+1][0]*prev_line + data[pix-(width*prev_line)-1][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)+1][1]*prev_line + data[pix-(width*prev_line)-1][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)+1][2]*prev_line + data[pix-(width*prev_line)-1][2]*next_line) / lines_lost)
                elif distance_tilt_right <= distance_horizontal and distance_horizontal <= distance_tilt_left:
                    newdata[0] = int((data[pix+(width*next_line)-1][0]*prev_line + data[pix-(width*prev_line)+1][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)-1][1]*prev_line + data[pix-(width*prev_line)+1][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)-1][2]*prev_line + data[pix-(width*prev_line)+1][2]*next_line) / lines_lost)            
                else:
                    newdata[0] = int((data[pix+(width*next_line)][0]*prev_line + data[pix-(width*prev_line)][0]*next_line) / lines_lost)
                    newdata[1] = int((data[pix+(width*next_line)][1]*prev_line + data[pix-(width*prev_line)][1]*next_line) / lines_lost)
                    newdata[2] = int((data[pix+(width*next_line)][2]*prev_line + data[pix-(width*prev_line)][2]*next_line) / lines_lost)      
                data[pix] = tuple(newdata)

#Save back to the file
res = Image.new(img.mode, img.size)
res.putdata(data)
res = res.convert("RGB")
print("Storing degradated image in", result_path)
res.save(result_path)
print_psnr(list(img.getdata()), data)
