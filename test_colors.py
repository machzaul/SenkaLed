#!/usr/bin/env python3
"""
test_colors.py
Script diagnostik untuk menguji tiap kanal warna (Merah, Hijau, Biru, Cyan)
pada panel LED HUB75 Raspberry Pi secara bergantian.
"""

import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1       # Tes di 1 panel dulu
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 4
options.brightness = 70
options.panel_type = "FM6127"  # Aktifkan driver IC P10

try:
    matrix = RGBMatrix(options=options)
except Exception as e:
    print(f"Error inisialisasi matrix: {e}")
    sys.exit(1)

colors = [
    ("MERAH MURNI (RED)", (255, 0, 0)),
    ("HIJAU MURNI (GREEN)", (0, 255, 0)),
    ("BIRU MURNI (BLUE)", (0, 0, 255)),
    ("CYAN MURNI (HIJAU + BIRU)", (0, 255, 255)),
    ("CYAN SENKA (#27CCF5)", (39, 204, 245))
]

print("=== MEMULAI TES DIAGNOSTIK WARNA LED ===")
print("Tekan Ctrl+C untuk berhenti kapan saja.\n")

try:
    for name, col in colors:
        print(f"-> Menampilkan: {name} - Nilai RGB: {col}")
        img = Image.new("RGB", (32, 16), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Gambar kotak penuh
        draw.rectangle((2, 2, 29, 13), fill=col)
        matrix.SetImage(img)
        time.sleep(3)

    print("\nTes selesai! Apakah warna Biru (BLUE) menyala di panel Anda?")
    time.sleep(1)
    matrix.Clear()

except KeyboardInterrupt:
    matrix.Clear()
    print("\nTes dihentikan.")
