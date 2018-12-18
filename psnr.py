"""
psnr.py

Functions to compute the PSNR

PSNR function adapted from https://github.com/magonzalezc/PSNRtool.

Francisco José Juaan Quintanilla, Jan-2018
See LICENSE.md in the root of the repository
"""

import math
import sys
from PIL import Image

def print_psnr(original_data, degradated_data):
    """
    This prints the Peak Signal to Noise Ratio (PSNR).
    :param original_data: As Pillow gives it with getdata
    :param degradated_data: As Pillow gives it with getdata
    :return:
    """
    psnr_y, psnr_cb, psnr_cr, psnr_avg = psnr(original_data, degradated_data)
    print('Y=', psnr_y, 'Cb=', psnr_cb, 'Cr=', psnr_cr,'Avg=',psnr_avg)

def psnr(original_data, degradated_data):
    """
    This calculates the Peak Signal to Noise Ratio (PSNR).
    :param original_data: As Pillow gives it with getdata
    :param degradated_data: As Pillow gives it with getdata
    :return: List containing the PSNR in Y, U, V and average of those 3
    """
    mse_y, mse_cb, mse_cr, mse_avg = mse(original_data, degradated_data)
    return psnr_from_mse([mse_y, mse_cb, mse_cr, mse_avg])

def mse(original_data, degradated_data):
    """
    This calculates the Mean Squared Error (MSE)
    :param original_data: As Pillow gives it with getdata
    :param degradated_data: As Pillow gives it with getdata
    :return: List containing the MSE in Y, U, V and average of those 3
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
    mse_avg = (mse_y*4 + mse_cb + mse_cr)/6

    return [mse_y, mse_cb, mse_cr, mse_avg]

    """
    Obtains the PSNR for a list of MSE values
    :param mse_list: A list of mse quantities
    :return: List containing the PSNR. If MSE is 0 the output PSNR is infinite
    """
def psnr_from_mse(mse_list):
    result = []

    for mse in mse_list:
        if  mse != 0:
            result.append(float(-10.0 * math.log(mse / (255 * 255), 10)))
        else:
            result.append(float('Inf'))
    return result

if __name__ == "__main__":

	img = Image.open(sys.argv[1])
	img = img.convert("YCbCr")
	
	img2 = Image.open(sys.argv[2])
	img2 = img2.convert("YCbCr")
	
	print_psnr(list(img.getdata()), list(img2.getdata()))
	
