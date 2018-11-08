"""
edge_interpolation.py

Francisco José Juan Quintanilla, Apr-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image
from psnr import print_psnr

#Settings
img_path = "img/ref/lena.bmp" #Path of the img
result_path = "img/out/lena-edgenew.bmp" #Path of the img interpolated
same_size = True #Same size image

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

# Step 1: Top line, top right and top left pixels included
x = 0
newdata[0]= data[x//2][0]
newdata[1]= data[x//2][1]
newdata[2]= data[x//2][2]
final_data[x] = tuple(newdata)

for x in range(1, final_width-1):
    if x % 2 == 0:
        newdata[0]= (3*data[x//2][0] + data[(x//2) - 1][0])//4
        newdata[1]= (3*data[x//2][1] + data[(x//2) - 1][1])//4
        newdata[2]= (3*data[x//2][2] + data[(x//2) - 1][2])//4
    else:
        newdata[0]= (3*data[x//2][0] + data[(x//2) + 1][0])//4
        newdata[1]= (3*data[x//2][1] + data[(x//2) + 1][1])//4
        newdata[2]= (3*data[x//2][2] + data[(x//2) + 1][2])//4
    final_data[x] = tuple(newdata)


x = final_width-1
newdata[0]= data[x//2][0]
newdata[1]= data[x//2][1]
newdata[2]= data[x//2][2]
final_data[x] = tuple(newdata)

# Step 2: Bottom line, bottom right and bottom left pixels included
y = final_height - 1
x = 0
newdata[0]= data[(y//2)*width + x//2][0]
newdata[1]= data[(y//2)*width + x//2][1]
newdata[2]= data[(y//2)*width + x//2][2]
final_data[y * final_width + x] = tuple(newdata)

for x in range (1, final_width - 1):
    if x % 2 == 0:
        newdata[0]= (3*data[(y//2)*width + x//2][0] + data[(y//2)*width + x//2 - 1][0])//4
        newdata[1]= (3*data[(y//2)*width + x//2][1] + data[(y//2)*width + x//2 - 1][1])//4
        newdata[2]= (3*data[(y//2)*width + x//2][2] + data[(y//2)*width + x//2 - 1][2])//4
    else:
        newdata[0]= (3*data[(y//2)*width + x//2][0] + data[(y//2)*width + x//2 + 1][0])//4
        newdata[1]= (3*data[(y//2)*width + x//2][1] + data[(y//2)*width + x//2 + 1][1])//4
        newdata[2]= (3*data[(y//2)*width + x//2][2] + data[(y//2)*width + x//2 + 1][2])//4
    final_data[y * final_width + x] = tuple(newdata) 

x = final_width-1
newdata[0]= data[(y//2)*width + x//2][0]
newdata[1]= data[(y//2)*width + x//2][1]
newdata[2]= data[(y//2)*width + x//2][2]
final_data[y * final_width + x] = tuple(newdata)

# Step 3: Left scanline
x = 0
for y in range (1, final_height - 1):
    if y % 2 == 0:
        newdata[0]= (3*data[(y//2)*width + x//2][0] + data[((y//2)-1)*width + x//2][0])//4
        newdata[1]= (3*data[(y//2)*width + x//2][1] + data[((y//2)-1)*width + x//2][1])//4
        newdata[2]= (3*data[(y//2)*width + x//2][2] + data[((y//2)-1)*width + x//2][2])//4
    else:
        newdata[0]= (3*data[(y//2)*width + x//2][0] + data[((y//2)+1)*width + x//2][0])//4
        newdata[1]= (3*data[(y//2)*width + x//2][1] + data[((y//2)+1)*width + x//2][1])//4
        newdata[2]= (3*data[(y//2)*width + x//2][2] + data[((y//2)+1)*width + x//2][2])//4
    final_data[y * final_width + x] = tuple(newdata) 

# Step 4: Right scanline
x = final_width -1
for y in range (1, final_height - 1):
    if y % 2 == 0:
        newdata[0]= (3*data[(y//2)*width + x//2][0] + data[((y//2)-1)*width + x//2][0])//4
        newdata[1]= (3*data[(y//2)*width + x//2][1] + data[((y//2)-1)*width + x//2][1])//4
        newdata[2]= (3*data[(y//2)*width + x//2][2] + data[((y//2)-1)*width + x//2][2])//4
    else:
        newdata[0]= (3*data[(y//2)*width + x//2][0] + data[((y//2)+1)*width + x//2][0])//4
        newdata[1]= (3*data[(y//2)*width + x//2][1] + data[((y//2)+1)*width + x//2][1])//4
        newdata[2]= (3*data[(y//2)*width + x//2][2] + data[((y//2)+1)*width + x//2][2])//4
    final_data[y * final_width + x] = tuple(newdata) 

# Step 5: Now lets do the first step of the edge algorithm. It copies the samples where those should be located. It includes the perpendicular between samples.
for y in range (1, final_height - 1):
    for x in range (1, final_width - 1):
        if  x % 2 == 0 and y % 2 == 0:
            newdata[0]= (9*data[(y//2)*width + x//2][0] + 4*data[((y//2)-1)*width + x//2][0] + 1*data[((y//2)-1)*width + x//2 - 1][0] + 4*data[(y//2)*width + x//2 - 1][0])//18
            newdata[1]= (9*data[(y//2)*width + x//2][1] + 4*data[((y//2)-1)*width + x//2][1] + 1*data[((y//2)-1)*width + x//2 - 1][1] + 4*data[(y//2)*width + x//2 - 1][1])//18
            newdata[2]= (9*data[(y//2)*width + x//2][2] + 4*data[((y//2)-1)*width + x//2][2] + 1*data[((y//2)-1)*width + x//2 - 1][2] + 4*data[(y//2)*width + x//2 - 1][2])//18
            final_data[y * final_width + x] = tuple(newdata)  
        elif x % 2 != 0 and y % 2 != 0:
            a = data[(y//2)*width + x//2][0]
            b = data[(y//2)*width + x//2 + 1][0]
            c = data[((y//2)+1)*width + x//2][0]
            d = data[((y//2)+1)*width + x//2 + 1][0]

            if abs(a - d) >= abs (b - c):
                newdata[0]= (b + c)//2
                newdata[1]= (data[(y//2)*width + x//2 + 1][1] + data[((y//2)+1)*width + x//2][1])//2
                newdata[2]= (data[(y//2)*width + x//2 + 1][2] + data[((y//2)+1)*width + x//2][2])//2
            else:
                newdata[0]= (9*a + 3*d)//12
                newdata[1]= (9*data[(y//2)*width + x//2][1] + 3*data[((y//2)+1)*width + x//2 + 1][1])//12
                newdata[2]= (9*data[(y//2)*width + x//2][2] + 3*data[((y//2)+1)*width + x//2 + 1][2])//12
            final_data[y * final_width + x] = tuple(newdata)            

# Step 5: Now lets do the second step of the edge algorithm. It is the horizontal and vertical of the image
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
if same_size:
    res2 = res.resize([width, height], Image.BILINEAR)
    res2.save(result_path)
else:
    res.save(result_path)
