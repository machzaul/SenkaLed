from panel import create_panel
from digital_font import DigitalFont

matrix = create_panel()

font = DigitalFont()

font.clear()

font.draw_digit(
    x=12,
    y=2,
    digit=8,
    color=(255,0,0)
)

matrix.SetImage(font.get_image())

input("Enter")

