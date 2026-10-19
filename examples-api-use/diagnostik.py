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

img = Image.new("RGB", (32,16))

pixels = img.load()

# bersihkan
for y in range(16):
    for x in range(32):
        pixels[x,y] = (0,0,0)

# garis horizontal
for y in range(16):
    color = (
        255 if y % 3 == 0 else 0,
        255 if y % 3 == 1 else 0,
        255 if y % 3 == 2 else 0
    )

    for x in range(32):
        pixels[x,y] = color

# garis vertikal putih tiap 4 pixel
for x in range(0,32,4):
    for y in range(16):
        pixels[x,y]=(255,255,255)

matrix.SetImage(img)

print("Diagnostic Pattern")
input("Enter untuk keluar")
