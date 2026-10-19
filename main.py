#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# ==========================================
# KONFIGURASI PANEL
# ==========================================

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 2

matrix = RGBMatrix(options=options)

# ==========================================
# FONT 3x5
# (nanti akan kita upgrade)
# ==========================================

FONT = {
'0':[
"111",
"101",
"101",
"101",
"111"],
'1':[
"010",
"110",
"010",
"010",
"111"],
'2':[
"111",
"001",
"111",
"100",
"111"],
'3':[
"111",
"001",
"111",
"001",
"111"],
'4':[
"101",
"101",
"111",
"001",
"001"],
'5':[
"111",
"100",
"111",
"001",
"111"],
'6':[
"111",
"100",
"111",
"101",
"111"],
'7':[
"111",
"001",
"001",
"001",
"001"],
'8':[
"111",
"101",
"111",
"101",
"111"],
'9':[
"111",
"101",
"111",
"001",
"111"],
}

# ==========================================

SCALE = 3

def draw_digit(px,digit,ox,oy,color):

    pattern = FONT[digit]

    for r,row in enumerate(pattern):
        for c,val in enumerate(row):

            if val=="1":

                for sy in range(SCALE):
                    for sx in range(SCALE):

                        x=ox+c*SCALE+sx
                        y=oy+r*SCALE+sy

                        if 0<=x<32 and 0<=y<16:
                            px[x,y]=color

# ==========================================

for angka in range(16):

    img=Image.new("RGB",(32,16),(0,0,0))
    px=img.load()

    teks=str(angka)

    if len(teks)==1:

        draw_digit(px,teks,11,0,(255,0,0))

    else:

        draw_digit(px,teks[0],4,0,(255,0,0))
        draw_digit(px,teks[1],18,0,(255,0,0))

    matrix.SetImage(img)

    time.sleep(1)

matrix.Clear()
