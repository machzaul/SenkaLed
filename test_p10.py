from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time

options = RGBMatrixOptions()

options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1

options.hardware_mapping = "regular"
options.panel_type = "FM6127"
options.gpio_slowdown = 4
options.brightness = 60

# Jika nanti panel tidak tampil, kita akan coba aktifkan ini:
# options.panel_type = "FM6126A"

matrix = RGBMatrix(options=options)

image = Image.new("RGB", (32, 16))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

draw.rectangle((0, 0, 31, 15), fill=(0, 0, 0))
draw.text((10, 4), "8", fill=(255, 0, 0), font=font)

matrix.SetImage(image)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    matrix.Clear()
