#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# ==========================
# Konfigurasi Panel
# ==========================
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

    for x in range(32):

        img = Image.new("RGB", (32,16), (0,0,0))
        pix = img.load()

        # Nyalakan SATU KOLOM
        for y in range(16):
            pix[x,y]=(255,0,0)

        matrix.SetImage(img)

        print(f"Testing Column : {x}")

        time.sleep(1)
