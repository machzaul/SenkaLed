#!/usr/bin/env python3
"""
display_engine.py
Engine rendering kanvas 96x16 untuk sistem display SenkaLed (3 panel P10).
Fitur Terbaru:
- Ukuran font seragam (Unified Font 3x5) untuk semua elemen teks & angka.
- Margin seimbang atas, bawah, kiri, dan kanan (tidak menempel ke tepi).
- Jarak rapat antara angka suhu (misal 35) dengan huruf 'C'.
- Warna paten: Biru Cyan Langit (#27CCF5).
"""

from PIL import Image

# Warna Biru Cyan Senka (lebih gelap & pekat, tidak terlalu pucat/terang)
COLOR_CYAN = (0, 130, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)

# ==============================================================================
# UNIFIED FONT MATRIKS (Tinggi seragam 5 pixel untuk seluruh teks & angka)
# ==============================================================================
FONT_UNIFIED = {
    ' ': ["00", "00", "00", "00", "00"],         # Lebar 2 px untuk spasi rapat
    '-': ["000", "000", "111", "000", "000"],
    '0': ["111", "101", "101", "101", "111"],
    '1': ["010", "110", "010", "010", "111"],
    '2': ["111", "001", "111", "100", "111"],
    '3': ["111", "001", "111", "001", "111"],
    '4': ["101", "101", "111", "001", "001"],
    '5': ["111", "100", "111", "001", "111"],
    '6': ["111", "100", "111", "101", "111"],
    '7': ["111", "001", "010", "010", "010"],
    '8': ["111", "101", "111", "101", "111"],
    '9': ["111", "101", "111", "001", "111"],
    'A': ["010", "101", "111", "101", "101"],
    'B': ["110", "101", "110", "101", "110"],
    'C': ["111", "100", "100", "100", "111"],
    'D': ["110", "101", "101", "101", "110"],
    'E': ["111", "100", "110", "100", "111"],
    'F': ["111", "100", "110", "100", "100"],
    'G': ["111", "100", "101", "101", "111"],
    'H': ["101", "101", "111", "101", "101"],
    'I': ["1", "1", "1", "1", "1"],             # Lebar 1 px ramping & presisi
    'J': ["001", "001", "001", "101", "010"],
    'K': ["101", "110", "100", "110", "101"],
    'L': ["100", "100", "100", "100", "111"],
    'M': ["101", "111", "101", "101", "101"],
    'N': ["111", "101", "101", "101", "101"],
    'O': ["111", "101", "101", "101", "111"],
    'P': ["111", "101", "111", "100", "100"],
    'Q': ["111", "101", "101", "111", "001"],
    'R': ["110", "101", "110", "101", "101"],
    'S': ["111", "100", "111", "001", "111"],
    'T': ["111", "010", "010", "010", "010"],
    'U': ["101", "101", "101", "101", "111"],
    'V': ["101", "101", "101", "101", "010"],
    'W': ["101", "101", "101", "111", "101"],
    'X': ["101", "101", "010", "101", "101"],
    'Y': ["101", "101", "111", "010", "010"],
    'Z': ["111", "001", "010", "100", "111"],
}


def measure_text_width(text, inter_char_gap=1):
    """Menghitung lebar pixel total suatu string teks."""
    if not text:
        return 0
    w = 0
    for i, ch in enumerate(text):
        pat = FONT_UNIFIED.get(ch, FONT_UNIFIED[' '])
        w += len(pat[0])
        if i < len(text) - 1:
            w += inter_char_gap
    return w


def draw_text(px, text, ox, oy, color, max_w=96, max_h=16, inter_char_gap=1):
    """Menggambar string teks bitmap ke pixel buffer PIL."""
    curr_x = ox
    for ch in text:
        pat = FONT_UNIFIED.get(ch, FONT_UNIFIED[' '])
        cw = len(pat[0])
        for r, row in enumerate(pat):
            for c, val in enumerate(row):
                if val == "1":
                    x = curr_x + c
                    y = oy + r
                    if 0 <= x < max_w and 0 <= y < max_h:
                        px[x, y] = color
        curr_x += cw + inter_char_gap


def render_senka_canvas(temperature=32, uv_index=7, uv_line1="VERY", uv_line2="HIGH", color=COLOR_CYAN):
    """
    Menghasilkan kanvas 96x16 pixel dengan spesifikasi:
    - Ukuran font seragam (tinggi 5 pixel untuk seluruh teks).
    - Margin atas & bawah seimbang (masing-masing 2 pixel).
    - Jarak rapat antara angka suhu dan 'C' (misal 32 C atau 35 C).
    - Margin kiri & kanan pada tiap panel (tidak mepet tepi).
    """
    img = Image.new("RGB", (96, 16), COLOR_BLACK)
    px = img.load()

    # Layout vertikal untuk display 2 baris (Panel 2 & 3):
    # - Margin Atas   : 2 px (Y: 0..1)
    # - Baris 1       : 5 px (Y: 2..6)
    # - Gap Tengah    : 2 px (Y: 7..8)
    # - Baris 2       : 5 px (Y: 9..13)
    # - Margin Bawah  : 2 px (Y: 14..15)
    y_row1 = 2
    y_row2 = 9

    # --------------------------------------------------------------------------
    # ZONA 1: PANEL 1 (X: 0 s/d 31) - SUHU ("35 C")
    # --------------------------------------------------------------------------
    # Suhu diformat dengan spasi rapat antara angka dan 'C'
    temp_text = f"{temperature} C"
    temp_w = measure_text_width(temp_text, inter_char_gap=1)
    # Center di Panel 1 (0..31) dengan margin kiri & kanan yang aman
    x_panel1 = (32 - temp_w) // 2
    # Center vertikal di 16 px (tinggi font 5 px -> offset Y: 5..6)
    y_panel1 = (16 - 5) // 2
    draw_text(px, temp_text, x_panel1, y_panel1, color, inter_char_gap=1)

    # --------------------------------------------------------------------------
    # ZONA 2: PANEL 2 (X: 32 s/d 63) - UV INDEX & ANGKA
    # --------------------------------------------------------------------------
    # Baris 1: "UV INDEX"
    uv_header = "UV INDEX"
    header_w = measure_text_width(uv_header, inter_char_gap=1)
    # Center di Panel 2 (32..63) -> margin kiri & kanan = (32 - 28) / 2 = 2 px
    x_header = 32 + (32 - header_w) // 2
    draw_text(px, uv_header, x_header, y_row1, color, inter_char_gap=1)

    # Baris 2: Nilai Angka UV
    uv_str = str(uv_index)
    uv_w = measure_text_width(uv_str, inter_char_gap=1)
    x_uv = 32 + (32 - uv_w) // 2
    draw_text(px, uv_str, x_uv, y_row2, color, inter_char_gap=1)

    # --------------------------------------------------------------------------
    # ZONA 3: PANEL 3 (X: 64 s/d 95) - SKALA BAHAYA UV (VERY / HIGH)
    # --------------------------------------------------------------------------
    # Baris 1: uv_line1 (misal "VERY" atau "UV")
    line1 = uv_line1.upper()
    line1_w = measure_text_width(line1, inter_char_gap=1)
    x_line1 = 64 + (32 - line1_w) // 2
    draw_text(px, line1, x_line1, y_row1, color, inter_char_gap=1)

    # Baris 2: uv_line2 (misal "HIGH" atau "LOW")
    line2 = uv_line2.upper()
    line2_w = measure_text_width(line2, inter_char_gap=1)
    x_line2 = 64 + (32 - line2_w) // 2
    draw_text(px, line2, x_line2, y_row2, color, inter_char_gap=1)

    return img


if __name__ == "__main__":
    img = render_senka_canvas(35, 9, "VERY", "HIGH")
    img.save("preview_test_96x16.png")
    print("Render test dengan ukuran font seragam & margin seimbang berhasil dibuat.")
