from panel import create_panel
from digital_font import DigitalFont

matrix = create_panel()

font = DigitalFont()

font.clear()

# Atas
font.draw_h_segment(
    x=8,
    y=2,
    length=16,
    thickness=2,
    color=(255,0,0)
)

# Kiri
font.draw_v_segment(
    x=8,
    y=2,
    thickness=2,
    length=12,
    color=(255,0,0)
)

matrix.SetImage(font.get_image())

input("Enter")

