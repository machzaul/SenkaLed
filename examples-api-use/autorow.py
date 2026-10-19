#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

FONT_PATH = "../fonts/5x8.bdf"

for row_type in range(6):

    print(f"\n==============================")
    print(f"Testing Row Address Type : {row_type}")
    print(f"==============================")

    options = RGBMatrixOptions()

    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1

    options.hardware_mapping = "regular"

    options.gpio_slowdown = 2

    options.multiplexing = 0

    options.row_address_type = row_type

    matrix = RGBMatrix(options=options)

    font = graphics.Font()
    font.LoadFont(FONT_PATH)

    red = graphics.Color(255,0,0)
    green = graphics.Color(0,255,0)

    canvas = matrix.CreateFrameCanvas()

    start = time.time()

    while time.time() - start < 5:

        canvas.Clear()

        # Menampilkan nomor row type
        graphics.DrawText(canvas,font,1,7,green,"TYPE")

        graphics.DrawText(canvas,font,10,15,red,str(row_type))

        canvas = matrix.SwapOnVSync(canvas)

    matrix.Clear()

print("\nSelesai.")
