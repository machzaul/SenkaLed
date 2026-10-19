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

img = Image.new("RGB",(32,16))

pix = img.load()

for y in range(16):
    for x in range(32):
        pix[x,y]=(0,0,0)

# gambar angka 8 manual
pts = [
(10,2),(11,2),(12,2),
(10,3),(12,3),
(10,4),(11,4),(12,4),
(10,5),(12,5),
(10,6),(11,6),(12,6)
]

for x,y in pts:
    pix[x,y]=(255,0,0)

matrix.SetImage(img)

input()
