#!/usr/bin/env python3
"""
display_engine.py
Engine rendering kanvas 96x16 untuk sistem display SenkaLed (3 panel P10).
Fitur Terbaru:
- Seluruh panel (3 panel) menggunakan format 2 Baris:
    * Panel 1: Baris 1 "TEMP", Baris 2 "{suhu} C"
    * Panel 2: Baris 1 "UV IDX", Baris 2 "{nilai_uv}"
    * Panel 3: Baris 1 "UV LVL", Baris 2 "{level_uv}" (LOW, MED, HIGH, VHI, EXT)
- Tipografi dibuat LEBIH TEBAL (BOLD) dengan goresan 2-pixel padat agar kontras tinggi.
- Fungsi render transisi lokasi (banner BLOK M dan CFD SUDIRMAN).
- Warna paten: Biru Cyan Senka (COLOR_CYAN = (0, 130, 255)).
"""

from PIL import Image

# Warna Biru Cyan Senka (pekat & kontras)
COLOR_CYAN = (0, 130, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)

# ==============================================================================
# FONT BOLD 6-PIXEL (Goresan tebal / bold 2-piksel untuk teks 2 baris)
# ==============================================================================
FONT_BOLD_6 = {
    'A': [
        "01110",
        "11011",
        "11111",
        "11011",
        "11011",
        "11011"
    ],
    'B': [
        "11110",
        "11011",
        "11110",
        "11011",
        "11011",
        "11110"
    ],
    'C': [
        "01111",
        "11000",
        "11000",
        "11000",
        "11000",
        "01111"
    ],
    'D': [
        "11110",
        "11011",
        "11011",
        "11011",
        "11011",
        "11110"
    ],
    'E': [
        "11111",
        "11000",
        "11110",
        "11000",
        "11000",
        "11111"
    ],
    'F': [
        "11111",
        "11000",
        "11110",
        "11000",
        "11000",
        "11000"
    ],
    'G': [
        "01111",
        "11000",
        "11011",
        "11011",
        "11011",
        "01111"
    ],
    'H': [
        "11011",
        "11011",
        "11111",
        "11011",
        "11011",
        "11011"
    ],
    'I': [
        "11",
        "11",
        "11",
        "11",
        "11",
        "11"
    ],
    'J': [
        "00011",
        "00011",
        "00011",
        "11011",
        "11011",
        "01110"
    ],
    'K': [
        "11011",
        "11110",
        "11100",
        "11110",
        "11011",
        "11011"
    ],
    'L': [
        "1100",
        "1100",
        "1100",
        "1100",
        "1100",
        "1111"
    ],
    'M': [
        "11011",
        "11111",
        "11011",
        "11011",
        "11011",
        "11011"
    ],
    'N': [
        "11011",
        "11111",
        "11111",
        "11111",
        "11011",
        "11011"
    ],
    'O': [
        "01110",
        "11011",
        "11011",
        "11011",
        "11011",
        "01110"
    ],
    'P': [
        "11110",
        "11011",
        "11110",
        "11000",
        "11000",
        "11000"
    ],
    'R': [
        "11110",
        "11011",
        "11110",
        "11100",
        "11011",
        "11011"
    ],
    'S': [
        "01111",
        "11000",
        "01110",
        "00011",
        "00011",
        "11110"
    ],
    'T': [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100"
    ],
    'U': [
        "11011",
        "11011",
        "11011",
        "11011",
        "11011",
        "01110"
    ],
    'V': [
        "11011",
        "11011",
        "11011",
        "11011",
        "01110",
        "00100"
    ],
    'W': [
        "11011",
        "11011",
        "11011",
        "11111",
        "11111",
        "01110"
    ],
    'X': [
        "11011",
        "11011",
        "01110",
        "01110",
        "11011",
        "11011"
    ],
    'Y': [
        "11011",
        "11011",
        "01110",
        "00100",
        "00100",
        "00100"
    ],
    ' ': [
        "00",
        "00",
        "00",
        "00",
        "00",
        "00"
    ],
    '-': [
        "000",
        "000",
        "111",
        "111",
        "000",
        "000"
    ],
    '0': [
        "01110",
        "11011",
        "11011",
        "11011",
        "11011",
        "01110"
    ],
    '1': [
        "0110",
        "1110",
        "0110",
        "0110",
        "0110",
        "1111"
    ],
    '2': [
        "11110",
        "00011",
        "01110",
        "11000",
        "11000",
        "11111"
    ],
    '3': [
        "11110",
        "00011",
        "01110",
        "00011",
        "00011",
        "11110"
    ],
    '4': [
        "11011",
        "11011",
        "11111",
        "00011",
        "00011",
        "00011"
    ],
    '5': [
        "11111",
        "11000",
        "11110",
        "00011",
        "00011",
        "11110"
    ],
    '6': [
        "01110",
        "11000",
        "11110",
        "11011",
        "11011",
        "01110"
    ],
    '7': [
        "11111",
        "00011",
        "00110",
        "01100",
        "01100",
        "01100"
    ],
    '8': [
        "01110",
        "11011",
        "01110",
        "11011",
        "11011",
        "01110"
    ],
    '9': [
        "01110",
        "11011",
        "01111",
        "00011",
        "00011",
        "01110"
    ]
}

# ==============================================================================
# FONT BOLD BESAR (Tinggi 10 pixel untuk Tampilan Banner Nama Lokasi BLOK M / CFD)
# ==============================================================================
FONT_BANNER_10 = {
    'B': ["11110", "11011", "11011", "11110", "11110", "11011", "11011", "11011", "11110", "11110"],
    'L': ["11000", "11000", "11000", "11000", "11000", "11000", "11000", "11000", "11111", "11111"],
    'O': ["01110", "11011", "11011", "11011", "11011", "11011", "11011", "11011", "11011", "01110"],
    'K': ["11011", "11110", "11100", "11110", "11011", "11011", "11011", "11011", "11011", "11011"],
    ' ': ["000", "000", "000", "000", "000", "000", "000", "000", "000", "000"],
    'M': ["110011", "111111", "110111", "110011", "110011", "110011", "110011", "110011", "110011", "110011"],
    'C': ["01111", "11000", "11000", "11000", "11000", "11000", "11000", "11000", "11000", "01111"],
    'F': ["11111", "11000", "11000", "11110", "11110", "11000", "11000", "11000", "11000", "11000"],
    'D': ["11110", "11011", "11011", "11011", "11011", "11011", "11011", "11011", "11011", "11110"],
    'S': ["01111", "11000", "11000", "01110", "00111", "00011", "00011", "00011", "11011", "01110"],
    'U': ["11011", "11011", "11011", "11011", "11011", "11011", "11011", "11011", "11011", "01110"],
    'I': ["11", "11", "11", "11", "11", "11", "11", "11", "11", "11"],
    'R': ["11110", "11011", "11011", "11110", "11100", "11110", "11011", "11011", "11011", "11011"],
    'A': ["01110", "11011", "11011", "11111", "11111", "11011", "11011", "11011", "11011", "11011"],
    'N': ["11011", "11111", "11111", "11111", "11011", "11011", "11011", "11011", "11011", "11011"]
}


def measure_text_width(text, font_dict=FONT_BOLD_6, inter_char_gap=1):
    """Menghitung total lebar pixel string teks."""
    if not text:
        return 0
    w = 0
    for i, ch in enumerate(text):
        pat = font_dict.get(ch, font_dict.get(' ', ["00"]*6))
        w += len(pat[0])
        if i < len(text) - 1:
            w += inter_char_gap
    return w


def draw_text(px, text, ox, oy, color, font_dict=FONT_BOLD_6, max_w=96, max_h=16, inter_char_gap=1):
    """Menggambar string teks bitmap ke buffer pixel PIL."""
    curr_x = ox
    for ch in text:
        pat = font_dict.get(ch, font_dict.get(' ', ["00"]*len(list(font_dict.values())[0])))
        cw = len(pat[0])
        for r, row in enumerate(pat):
            for c, val in enumerate(row):
                if val == "1":
                    x = curr_x + c
                    y = oy + r
                    if 0 <= x < max_w and 0 <= y < max_h:
                        px[x, y] = color
        curr_x += cw + inter_char_gap


def render_senka_canvas(temperature=32, uv_index=7, uv_level="VHI", color=COLOR_CYAN):
    """
    Menghasilkan kanvas 96x16 pixel dengan spesifikasi terbaru:
    - Seluruh panel 2 baris (tinggi font 6 px, tebal/bold):
        * Panel 1 (0..31)  : Baris 1 "TEMP",   Baris 2 "{temperature} C"
        * Panel 2 (32..63) : Baris 1 "UV IDX", Baris 2 "{uv_index}"
        * Panel 3 (64..95) : Baris 1 "UV LVL", Baris 2 "{uv_level}" (LOW, MED, HIGH, VHI, EXT)
    - Posisi vertikal:
        * Baris 1 : Y = 1
        * Baris 2 : Y = 9
    """
    img = Image.new("RGB", (96, 16), COLOR_BLACK)
    px = img.load()

    y_row1 = 1
    y_row2 = 9

    # --------------------------------------------------------------------------
    # PANEL 1 (X: 0 s/d 31) - SUHU
    # Baris 1: "TEMP"
    # Baris 2: "{suhu} C"
    # --------------------------------------------------------------------------
    p1_row1 = "TEMP"
    p1_row1_w = measure_text_width(p1_row1, FONT_BOLD_6, inter_char_gap=1)
    x1_r1 = (32 - p1_row1_w) // 2
    draw_text(px, p1_row1, x1_r1, y_row1, color, FONT_BOLD_6, inter_char_gap=1)

    p1_row2 = f"{temperature} C"
    p1_row2_w = measure_text_width(p1_row2, FONT_BOLD_6, inter_char_gap=1)
    x1_r2 = (32 - p1_row2_w) // 2
    draw_text(px, p1_row2, x1_r2, y_row2, color, FONT_BOLD_6, inter_char_gap=1)

    # --------------------------------------------------------------------------
    # PANEL 2 (X: 32 s/d 63) - UV INDEX
    # Baris 1: "UV IDX"
    # Baris 2: "{uv_index}"
    # --------------------------------------------------------------------------
    p2_row1 = "UV IDX"
    p2_row1_w = measure_text_width(p2_row1, FONT_BOLD_6, inter_char_gap=1)
    x2_r1 = 32 + (32 - p2_row1_w) // 2
    draw_text(px, p2_row1, x2_r1, y_row1, color, FONT_BOLD_6, inter_char_gap=1)

    p2_row2 = str(uv_index)
    p2_row2_w = measure_text_width(p2_row2, FONT_BOLD_6, inter_char_gap=1)
    x2_r2 = 32 + (32 - p2_row2_w) // 2
    draw_text(px, p2_row2, x2_r2, y_row2, color, FONT_BOLD_6, inter_char_gap=1)

    # --------------------------------------------------------------------------
    # PANEL 3 (X: 64 s/d 95) - UV LEVEL (RINGKAS: LOW, MED, HIGH, VHI, EXT)
    # Baris 1: "UV LVL"
    # Baris 2: "{uv_level}"
    # --------------------------------------------------------------------------
    p3_row1 = "UV LVL"
    p3_row1_w = measure_text_width(p3_row1, FONT_BOLD_6, inter_char_gap=1)
    x3_r1 = 64 + (32 - p3_row1_w) // 2
    draw_text(px, p3_row1, x3_r1, y_row1, color, FONT_BOLD_6, inter_char_gap=1)

    p3_row2 = str(uv_level).upper()
    p3_row2_w = measure_text_width(p3_row2, FONT_BOLD_6, inter_char_gap=1)
    x3_r2 = 64 + (32 - p3_row2_w) // 2
    draw_text(px, p3_row2, x3_r2, y_row2, color, FONT_BOLD_6, inter_char_gap=1)

    return img


def render_location_banner(location_name="BLOK M", color=COLOR_CYAN):
    """
    Menghasilkan layar transisi banner tebal ukuran penuh 96x16
    saat tombol pemindah lokasi ditekan (misal: "BLOK M" atau "CFD SUDIRMAN").
    """
    img = Image.new("RGB", (96, 16), COLOR_BLACK)
    px = img.load()

    loc_str = location_name.upper().strip()

    # Jika nama lokasi "BLOK M", gunakan font banner besar (tinggi 10 px)
    if loc_str == "BLOK M":
        w = measure_text_width(loc_str, FONT_BANNER_10, inter_char_gap=2)
        start_x = (96 - w) // 2
        start_y = 3
        draw_text(px, loc_str, start_x, start_y, color, FONT_BANNER_10, inter_char_gap=2)
    else:
        # Jika nama lokasi "CFD SUDIRMAN" atau lainnya
        w = measure_text_width(loc_str, FONT_BOLD_6, inter_char_gap=1)
        if w <= 94:
            start_x = (96 - w) // 2
            start_y = 5
            draw_text(px, loc_str, start_x, start_y, color, FONT_BOLD_6, inter_char_gap=1)
        else:
            # Fallback 2 baris jika sangat panjang
            r1 = "CFD"
            r2 = "SUDIRMAN"
            w1 = measure_text_width(r1, FONT_BOLD_6, inter_char_gap=1)
            w2 = measure_text_width(r2, FONT_BOLD_6, inter_char_gap=1)
            draw_text(px, r1, (96 - w1)//2, 1, color, FONT_BOLD_6)
            draw_text(px, r2, (96 - w2)//2, 9, color, FONT_BOLD_6)

    return img


if __name__ == "__main__":
    # Test render kanvas utama 2 baris
    img_main = render_senka_canvas(32, 9, "VHI")
    img_main.save("preview_2row_bold.png")
    print("Test render kanvas 2 baris tebal berhasil: preview_2row_bold.png")

    # Test render banner BLOK M
    img_blokm = render_location_banner("BLOK M")
    img_blokm.save("preview_banner_blokm.png")
    print("Test render banner BLOK M berhasil: preview_banner_blokm.png")

    # Test render banner CFD SUDIRMAN
    img_cfd = render_location_banner("CFD SUDIRMAN")
    img_cfd.save("preview_banner_cfd.png")
    print("Test render banner CFD SUDIRMAN berhasil: preview_banner_cfd.png")
