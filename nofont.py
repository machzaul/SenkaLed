#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import time

for row_type in [0,1,2,3,4,5]:
    print("ROW ADDRESS =", row_type)

    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    options.gpio_slowdown = 2
    options.row_address_type = row_type

    matrix = RGBMatrix(options=options)

    img = Image.new("RGB",(32,16))
    px = img.load()

    for y in range(16):
        for x in range(32):
            px[x,y]=(0,0,0)

    # hanya nyalakan baris nomor 0
    for x in range(32):
        px[x,0]=(255,0,0)

    matrix.SetImage(img)

    input(f"RowType {row_type}  -> Enter")
