#!/usr/bin/env python3

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

# ==========================
# Gambar
# ==========================
img = Image.new("RGB", (32, 16), (255, 255, 255))
pixels = img.load()

# ======================================================
# MATIKAN BARIS DI SINI
#
# Ganti angka menjadi nomor baris yang ingin dimatikan
#
# Contoh:
# rows_off = []
# rows_off = [0]
# rows_off = [0,1]
# rows_off = [4]
# rows_off = [4,5,6]
#
# Nomor baris:
#
#  0
#  1
#  2
#  3
#  4
#  5
#  6
#  7
#  8
#  9
# 10
# 11
# 12
# 13
# 14
# 15
# ======================================================

rows_off = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

# ======================================================

for y in rows_off:
    if 0 <= y < 16:
        for x in range(32):
            pixels[x, y] = (0, 0, 0)

matrix.SetImage(img)

print("Panel aktif")
print("Rows OFF :", rows_off)

input("Enter untuk keluar...")
