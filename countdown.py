#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# ============================================
# KONFIGURASI PANEL
# ============================================

options = RGBMatrixOptions()

options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"
options.gpio_slowdown = 2

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()

# ============================================
# FONT
# ============================================

font = graphics.Font()
font.LoadFont("fonts/5x8.bdf")

color = graphics.Color(255, 0, 0)

# ============================================
# COUNTDOWN
# ============================================

START_TIME = 15.0

start = time.perf_counter()

while True:

    elapsed = time.perf_counter() - start
    remain = START_TIME - elapsed

    if remain < 0:
        remain = 0

    second = int(remain)

    centisecond = int((remain - second) * 100)

    text = f"{second:02d}:{centisecond:02d}"

    canvas.Clear()

    graphics.DrawText(
        canvas,
        font,
        1,      # X
        12,     # Y
        color,
        text
    )

    canvas = matrix.SwapOnVSync(canvas)

    if remain <= 0:
        break

matrix.Clear()
