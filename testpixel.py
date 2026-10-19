#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 2

matrix = RGBMatrix(options=options)

img = Image.new("RGB", (32, 16), (0, 0, 0))

# Nyalakan SATU pixel kiri atas
img.putpixel((0, 0), (255, 0, 0))

matrix.SetImage(img)

input("Tekan Enter untuk keluar...")
