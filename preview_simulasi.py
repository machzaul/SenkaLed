#!/usr/bin/env python3
"""
preview_simulasi.py
Membuat simulasi visual tampilan SenkaLed 96x16 pixel dengan layout terbaru:
- Tampilan Utama 2 Baris Tebal (TEMP, UV IDX, UV LVL).
- Tampilan Layar Transisi Banner BLOK M dan CFD SUDIRMAN.
- Menghasilkan simulasi LED Matrix HD (dot melingkar) untuk peninjauan di PC.
"""

import os
from PIL import Image, ImageDraw
from display_engine import render_senka_canvas, render_location_banner, COLOR_CYAN
from weather_service import WeatherService


def create_led_matrix_simulation(src_img, dot_size=10, gap=2, bg_color=(10, 14, 20)):
    """Mengonversi gambar pixel 96x16 menjadi simulasi fisik dot LED Matrix."""
    w, h = src_img.size
    cell_size = dot_size + gap
    out_w = w * cell_size + gap
    out_h = h * cell_size + gap

    sim_img = Image.new("RGB", (out_w, out_h), bg_color)
    draw = ImageDraw.Draw(sim_img)
    src_px = src_img.load()

    for y in range(h):
        for x in range(w):
            r, g, b = src_px[x, y]
            x0 = gap + x * cell_size
            y0 = gap + y * cell_size
            x1 = x0 + dot_size
            y1 = y0 + dot_size

            if (r, g, b) != (0, 0, 0):
                draw.ellipse([x0, y0, x1, y1], fill=(r, g, b), outline=(min(255, r+30), min(255, g+30), min(255, b+30)))
            else:
                draw.ellipse([x0, y0, x1, y1], fill=(20, 24, 30), outline=(15, 18, 22))

    return sim_img


def generate_all_previews():
    ws = WeatherService()
    print("[Preview] Mengambil data cuaca real-time untuk Blok M dan CFD...")
    ws.fetch_all()
    
    # 1. Preview Tampilan Utama 2 Baris (Data Blok M)
    data = ws.get_current()
    temp = data["temperature"]
    uv = data["uv_index"]
    level = data["uv_level"]
    print(f" -> Render Layar Utama 2 Baris: TEMP {temp}°C | UV IDX {uv} | UV LVL {level}")
    
    img_main = render_senka_canvas(temp, uv, level, COLOR_CYAN)
    img_main_hd = create_led_matrix_simulation(img_main, dot_size=10, gap=3)
    img_main_hd.save("preview_senkaled_2row_bold.png")
    img_main.save("preview_senkaled_actual.png")

    # 2. Preview Banner Transisi BLOK M
    print(" -> Render Banner Transisi: BLOK M")
    img_blokm = render_location_banner("BLOK M", COLOR_CYAN)
    img_blokm_hd = create_led_matrix_simulation(img_blokm, dot_size=10, gap=3)
    img_blokm_hd.save("preview_senkaled_banner_blokm.png")

    # 3. Preview Banner Transisi CFD SUDIRMAN
    print(" -> Render Banner Transisi: CFD SUDIRMAN")
    img_cfd = render_location_banner("CFD SUDIRMAN", COLOR_CYAN)
    img_cfd_hd = create_led_matrix_simulation(img_cfd, dot_size=10, gap=3)
    img_cfd_hd.save("preview_senkaled_banner_cfd.png")

    # Salin ke folder artifact untuk ditampilkan ke user
    artifact_dir = r"C:\Users\USER\.gemini\antigravity\brain\df4c96da-b715-4972-82fd-243c5bf03747"
    if os.path.exists(artifact_dir):
        img_main_hd.save(os.path.join(artifact_dir, "preview_senkaled_2row_bold.png"))
        img_blokm_hd.save(os.path.join(artifact_dir, "preview_senkaled_banner_blokm.png"))
        img_cfd_hd.save(os.path.join(artifact_dir, "preview_senkaled_banner_cfd.png"))
        print("[Preview] Seluruh file simulasi berhasil disalin ke folder artifact.")


if __name__ == "__main__":
    generate_all_previews()
