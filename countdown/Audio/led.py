from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"

matrix = RGBMatrix(options=options)

# Font bawaan
font = ImageFont.load_default()

image = Image.new("RGB", (32, 16))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 31, 15), fill=(0, 0, 0))
draw.text((10, 4), "8", fill=(255, 0, 0), font=font)

matrix.SetImage(image)

input("Tekan Enter untuk keluar...")