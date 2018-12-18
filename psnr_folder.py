"""
psnr_folder.py

Francisco José Juan Quintanilla, Nov-2018
See LICENSE.md in the root of the repository
"""

from PIL import Image
from psnr import mse, psnr_from_mse
import os

#Settings
reference_path = "img/ref" #Path of the img
degradated_path = "img/out" #Path of the img interpolated

###############################
#Start of the script
###############################

print("Comparing folder", reference_path, "with",degradated_path)

#Folder opening and checking
ref_files = os.listdir(reference_path);
deg_files = os.listdir(degradated_path);

#Remove folders, leave only files
for entry in ref_files:
    path = reference_path + os.sep + entry
    if (not os.access(path, os.F_OK)) or (not os.path.isfile(path)):
       ref_files.remove(entry) 
		

for entry in deg_files:
    path =  degradated_path + os.sep + entry
    if (not os.access(path, os.F_OK)) or (not os.path.isfile(path)):
        deg_files.remove(entry) 

#Remove files that are not present in the degradated folder
not_found_files=0
files = []

for ref_filename in ref_files:
    found = False
    for deg_filename in deg_files:
        if ref_filename == deg_filename:
            found = True
    if found:
        files.append(ref_filename)

print("Reference folder contains",len(ref_files),"elements. Of those ",len(files), "were found in the degradated folder.")
sum_mseY = 0
max_mseY = 0
min_mseY = 999999
sum_mseU = 0
max_mseU = 0
min_mseU = 999999
sum_mseV = 0
max_mseV = 0
min_mseV = 999999
sum_mseFrm = 0
max_mseFrm = 0
min_mseFrm = 999999

index =0
for filename in files:
    if index % 10 == 0:
        print("Processing picture", index , "of",len(files))
    ref_img = Image.open(reference_path+ os.sep+filename)
    ref_img = ref_img.convert("YCbCr")

    deg_img = Image.open(degradated_path+ os.sep+filename)
    deg_img = deg_img.convert("YCbCr")

    mseY, mseU, mseV, mseFrm = mse(list(ref_img.getdata()), list(deg_img.getdata()))

    sum_mseY =sum_mseY + mseY
    sum_mseU =sum_mseU + mseU
    sum_mseV =sum_mseV + mseV
    sum_mseFrm = sum_mseFrm + mseFrm

    if mseY > max_mseY:
        max_mseY = mseY
    if mseU > max_mseU:
        max_mseU = mseU
    if mseV > max_mseV:
        max_mseV = mseV        
    if mseFrm > max_mseFrm:
        max_mseFrm = mseFrm 

    if mseY < min_mseY:
        min_mseY = mseY
    if mseU < min_mseU:
        min_mseU = mseU
    if mseV < min_mseV:
        min_mseV = mseV
    if mseFrm < min_mseFrm:
        min_mseFrm = mseFrm

    index = index + 1

sum_mseY = sum_mseY/len(ref_files)
sum_mseU = sum_mseU/len(ref_files)
sum_mseV = sum_mseV/len(ref_files)
sum_mseFrm = sum_mseFrm/len(ref_files)

psnr_y, psnr_u, psnr_v, psnr_avg=psnr_from_mse([sum_mseY, sum_mseU, sum_mseV, sum_mseFrm])

print ("Averaging all: PSNR_Y=", psnr_y, "PSNR_U=", psnr_u,"PSNR_V=",psnr_v, "PSNR_Im=", psnr_avg)
