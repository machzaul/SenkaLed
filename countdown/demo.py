from panel import create_panel
from digital_font import DigitalFont

matrix = create_panel()

font = DigitalFont()

font.clear()

# Kotak merah ukuran 10x10
x = font.center_x(10)   # koreksi visual 1 pixel ke kiri
y = font.center_y(10)

font.draw_box(
    x=x,
    y=y,
    w=10,
    h=10,
    color=(255,0,0)
)

matrix.SetImage(font.get_image())

input("Enter")
