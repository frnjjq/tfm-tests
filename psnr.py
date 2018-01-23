"""
psnr.py

Functions to compute the PSNR

PSNR function adapted from https://github.com/magonzalezc/PSNRtool.

Francisco José Juaan Quintanilla, Jan-2018
See LICENSE.md in the root of the repository
"""

import math

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

def psnr(original_data, degradated_data):
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

    return [psnr_y, psnr_cb, psnr_cr]