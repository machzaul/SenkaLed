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

pixels=img.load()

for y in range(16):
    for x in range(32):

        if y==0:
            pixels[x,y]=(255,0,0)

        elif y==1:
            pixels[x,y]=(0,255,0)

        elif y==2:
            pixels[x,y]=(0,0,255)

        elif y==3:
            pixels[x,y]=(255,255,0)

        elif y==4:
            pixels[x,y]=(255,0,255)

        elif y==5:
            pixels[x,y]=(0,255,255)

        elif y==6:
            pixels[x,y]=(255,255,255)

        elif y==7:
            pixels[x,y]=(255,120,0)

        else:
            pixels[x,y]=(0,0,0)

matrix.SetImage(img)

input("Enter")
