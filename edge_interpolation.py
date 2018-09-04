"""
edge_interpolation.py

Francisco José Juan Quintanilla, Apr-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image
from psnr import print_psnr

#Settings
img_path = "img/ref/lena_128.bmp" #Path of the img
result_path = "img/out/lena_128-edge.bmp" #Path of the img interpolated

###############################
#Start of the script
###############################

print("Taking image from", img_path)
#Image opening and extracting
img = Image.open(img_path)
img = img.convert("YCbCr")
width, height = img.size
data = list(img.getdata())
newdata = [0, 0, 0]
final_width = width *2
final_height = height*2
final_data = [0] * final_width * final_height

for x in range(final_width-1):
    if x % 2 == 0:
        newdata[0]= data[x//2][0]
        newdata[1]= data[x//2][1]
        newdata[2]= data[x//2][2]
    else:
        newdata[0]= (data[x//2][0] + data[(x//2) + 1][0])//2
        newdata[1]= (data[x//2][1] + data[(x//2) + 1][1])//2
        newdata[2]= (data[x//2][2] + data[(x//2) + 1][2])//2
    final_data[x] = tuple(newdata)


x = final_width-1
newdata[0]= data[x//2][0]
newdata[1]= data[x//2][1]
newdata[2]= data[x//2][2]
final_data[x] = tuple(newdata)

y = final_height - 1
for x in range (final_width - 1):
    if x % 2 == 0:
        newdata[0]= data[(y//2)*width + x//2][0]
        newdata[1]= data[(y//2)*width + x//2][1]
        newdata[2]= data[(y//2)*width + x//2][2]
    else:
        newdata[0]= (data[(y//2)*width + x//2][0] + data[(y//2)*width + x//2 + 1][0])//2
        newdata[1]= (data[(y//2)*width + x//2][1] + data[(y//2)*width + x//2 + 1][1])//2
        newdata[2]= (data[(y//2)*width + x//2][2] + data[(y//2)*width + x//2 + 1][2])//2
    final_data[y * final_width + x] = tuple(newdata) 

x = final_width-1
newdata[0]= data[(y//2)*width + x//2][0]
newdata[1]= data[(y//2)*width + x//2][1]
newdata[2]= data[(y//2)*width + x//2][2]
final_data[y * final_width + x] = tuple(newdata)

x = 0
for y in range (1, final_height - 1):
    if y % 2 == 0:
        newdata[0]= data[(y//2)*width + x//2][0]
        newdata[1]= data[(y//2)*width + x//2][1]
        newdata[2]= data[(y//2)*width + x//2][2]
    else:
        newdata[0]= (data[(y//2)*width + x//2][0] + data[((y//2)+1)*width + x//2][0])//2
        newdata[1]= (data[(y//2)*width + x//2][1] + data[((y//2)+1)*width + x//2][1])//2
        newdata[2]= (data[(y//2)*width + x//2][2] + data[((y//2)+1)*width + x//2][2])//2
    final_data[y * final_width + x] = tuple(newdata) 

x = final_width -1
for y in range (1, final_height - 1):
    if y % 2 == 0:
        newdata[0]= data[(y//2)*width + x//2][0]
        newdata[1]= data[(y//2)*width + x//2][1]
        newdata[2]= data[(y//2)*width + x//2][2]
    else:
        newdata[0]= (data[(y//2)*width + x//2][0] + data[((y//2)+1)*width + x//2][0])//2
        newdata[1]= (data[(y//2)*width + x//2][1] + data[((y//2)+1)*width + x//2][1])//2
        newdata[2]= (data[(y//2)*width + x//2][2] + data[((y//2)+1)*width + x//2][2])//2
    final_data[y * final_width + x] = tuple(newdata) 

for y in range (1, final_height - 1):
    for x in range (1, final_width - 1):
        if  x % 2 == 0 and y % 2 == 0:
            newdata[0]= data[(y//2)*width + x//2][0]
            newdata[1]= data[(y//2)*width + x//2][1]
            newdata[2]= data[(y//2)*width + x//2][2]
            final_data[y * final_width + x] = tuple(newdata)  
        elif x % 2 != 0 and y % 2 != 0:
            a = data[(y//2)*width + x//2][0]
            b = data[(y//2)*width + x//2 + 1][0]
            c = data[((y//2)+1)*width + x//2][0]
            d = data[((y//2)+1)*width + x//2 + 1][0]

            if abs(a - d) >= abs (b -c):
                newdata[0]= (data[(y//2)*width + x//2 + 1][0] + data[((y//2)+1)*width + x//2][0])//2
                newdata[1]= (data[(y//2)*width + x//2 + 1][1] + data[((y//2)+1)*width + x//2][1])//2
                newdata[2]= (data[(y//2)*width + x//2 + 1][2] + data[((y//2)+1)*width + x//2][2])//2
            else:
                newdata[0]= (data[(y//2)*width + x//2][0] + data[((y//2)+1)*width + x//2 + 1][0])//2
                newdata[1]= (data[(y//2)*width + x//2][1] + data[((y//2)+1)*width + x//2 + 1][1])//2
                newdata[2]= (data[(y//2)*width + x//2][2] + data[((y//2)+1)*width + x//2 + 1][2])//2
            final_data[y * final_width + x] = tuple(newdata)            

for y in range (1, final_height - 1):
    for x in range (1, final_width - 1):
        if  (x % 2 == 0 and y % 2 != 0) or (x % 2 != 0 and y % 2 == 0):
            a = final_data[(y-1)*final_width + x][0]
            b = final_data[y*final_width + x + 1][0]
            c = final_data[(y+1)*final_width + x][0]
            d = final_data[y*final_width + x - 1][0]

            if abs(a - c) >= abs(b - d):
                newdata[0]= (final_data[y*final_width + x + 1][0] + final_data[y*final_width + x - 1][0])//2
                newdata[1]= (final_data[y*final_width + x + 1][1] + final_data[y*final_width + x - 1][1])//2
                newdata[2]= (final_data[y*final_width + x + 1][2] + final_data[y*final_width + x - 1][2])//2
            else:
                newdata[0]= (final_data[(y-1)*final_width + x][0] + final_data[(y+1)*final_width + x][0])//2
                newdata[1]= (final_data[(y-1)*final_width + x][1] + final_data[(y+1)*final_width + x][1])//2
                newdata[2]= (final_data[(y-1)*final_width + x][2] + final_data[(y+1)*final_width + x][2])//2
            final_data[y * final_width + x] = tuple(newdata)

#Save back to the file
res = Image.new(img.mode, [final_width, final_height])
res.putdata(final_data)
res = res.convert("RGB")
print("Storing degradated image in", result_path)
res.save(result_path)
