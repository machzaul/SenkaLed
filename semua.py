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

img = Image.new("RGB", (32, 16), (0, 0, 0))
pix = img.load()

# ==========================
# Grid
# ==========================

# Garis vertikal putih
for x in range(32):
    if x % 2 == 0:
        for y in range(16):
            pix[x, y] = (80, 80, 80)

# Garis horizontal putih
for y in range(16):
    if y % 2 == 0:
        for x in range(32):
            pix[x, y] = (80, 80, 80)

# ==========================
# Titik Referensi
# ==========================

# Empat sudut
pix[0,0]     = (255,0,0)      # kiri atas
pix[31,0]    = (0,255,0)      # kanan atas
pix[0,15]    = (0,0,255)      # kiri bawah
pix[31,15]   = (255,255,0)    # kanan bawah

# Tengah
pix[16,8] = (255,0,255)

matrix.SetImage(img)

print("Grid 32x16 aktif")
input("Tekan Enter...")
