#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions

options = RGBMatrixOptions()

options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 2

print("Sebelum membuat matrix")

matrix = RGBMatrix(options=options)

print("Matrix berhasil dibuat")

