"""
psnr_folder.py

Francisco José Juan Quintanilla, Nov-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image
from psnr import psnr, psnr_np
import os

#Settings
reference_path = "/home/pi/Videos/test/framessintel" #Path of the img
degradated_path = "/home/pi/Videos/out/sintel-spsnedge" #Path of the img interpolated

###############################
#Start of the script
###############################

print("Comparing folder", reference_path, "with",degradated_path)

#Folder opening and checking
ref_files = os.listdir(reference_path);
deg_files = os.listdir(degradated_path);

for entry in ref_files:
    path = reference_path + os.sep + entry
    if (not os.access(path, os.F_OK)) or (not os.path.isfile(path)):
       ref_files.remove(entry) 
		

for entry in deg_files:
    path =  degradated_path + os.sep + entry
    if (not os.access(path, os.F_OK)) or (not os.path.isfile(path)):
        deg_files.remove(entry) 
	
count_files = len(ref_files)
not_found_files=0
for filename in ref_files:
    if filename not in deg_files:
        not_found_files = not_found_files+1
        ref_files.remove(filename) 

print("Reference folder contains",count_files,"elements. Of those ",not_found_files, "were not found in the degradated folder.")
sum_psnrY = 0
max_psnrY = 0
min_psnrY = 600
sum_psnrU = 0
max_psnrU = 0
min_psnrU = 600
sum_psnrV = 0
max_psnrV = 0
min_psnrV = 600

index =0
for filename in ref_files:
    if index % 10 == 0:
        print("Processing picture", index , "of",count_files)
    ref_img = Image.open(reference_path+ os.sep+filename)
    ref_img = ref_img.convert("YCbCr")

    deg_img = Image.open(degradated_path+ os.sep+filename)
    deg_img = deg_img.convert("YCbCr")

    psnrY, psnrU, psnrV =psnr_np(list(ref_img.getdata()), list(deg_img.getdata()))
    sum_psnrY = sum_psnrY+psnrY
    if psnrY > max_psnrY:
        max_psnrY = psnrY
    if psnrY < min_psnrY:
        min_psnrY = psnrY
        
    sum_psnrU = sum_psnrU+psnrU
    if psnrU > max_psnrU:
        max_psnrU = psnrU
    if psnrU < min_psnrU:
        min_psnrU = psnrU
          
    sum_psnrV = sum_psnrV+psnrV
    if psnrV > max_psnrV:
        max_psnrV = psnrV
    if psnrV < min_psnrV:
        min_psnrV = psnrV
    index = index + 1
sum_psnrY = sum_psnrY/len(ref_files)
sum_psnrU = sum_psnrU/len(ref_files)
sum_psnrV = sum_psnrV/len(ref_files)


print ("Avg{",sum_psnrY,sum_psnrU,sum_psnrV,"} Max:{",max_psnrY,max_psnrU,max_psnrV,"} Min:{",min_psnrY,min_psnrU,min_psnrV)
