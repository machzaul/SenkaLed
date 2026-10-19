#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 2
options.multiplexing = 0

matrix = RGBMatrix(options=options)

while True:

    for y in range(16):

        img = Image.new("RGB", (32,16), (0,0,0))
        pix = img.load()

        # Nyalakan SATU BARIS
        for x in range(32):
            pix[x,y]=(0,255,0)

        matrix.SetImage(img)

        print(f"Testing Row : {y}")

        time.sleep(1)
