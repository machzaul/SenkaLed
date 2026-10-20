#!/usr/bin/env python3
"""
preview_simulasi.py
Membuat simulasi visual tampilan SenkaLed 96x16 pixel baik dalam resolusi asli
maupun resolusi simulasi LED Matrix HD (dengan grid dot LED melingkar)
sehingga bisa langsung dilihat hasilnya di komputer/laptop.
"""

import os
from PIL import Image, ImageDraw
from display_engine import render_senka_canvas, COLOR_CYAN
from weather_service import WeatherService


def create_led_matrix_simulation(src_img, dot_size=10, gap=2, bg_color=(10, 14, 20)):
    """
    Mengonversi gambar pixel 96x16 menjadi simulasi fisik LED Matrix
    lengkap dengan dot LED bulat dan grid gelap antar pixel.
    """
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

            # Jika pixel menyala
            if (r, g, b) != (0, 0, 0):
                # Lingkaran LED menyala
                draw.ellipse([x0, y0, x1, y1], fill=(r, g, b), outline=(min(255, r+30), min(255, g+30), min(255, b+30)))
            else:
                # LED mati (abu-abu sangat gelap khas panel P10)
                draw.ellipse([x0, y0, x1, y1], fill=(20, 24, 30), outline=(15, 18, 22))

    return sim_img


def generate_all_previews():
    ws = WeatherService()
    # Coba fetch data real-time Jakarta
    print("[Preview] Mengambil data cuaca Jakarta...")
    ws.fetch_data()
    data = ws.get_current()
    temp = data["temperature"]
    uv = data["uv_index"]
    line1 = data["uv_line1"]
    line2 = data["uv_line2"]

    print(f"[Preview] Menghasilkan simulasi dengan data: {temp}°C, UV {uv} ({line1} {line2})")

    # 1. Render Kanvas Asli 96x16
    img_actual = render_senka_canvas(temp, uv, line1, line2, COLOR_CYAN)
    actual_path = "preview_senkaled_actual.png"
    img_actual.save(actual_path)
    print(f" -> Tersimpan: {actual_path} (96x16 pixel)")

    # 2. Render Kanvas Simulasi LED Matrix HD
    img_hd = create_led_matrix_simulation(img_actual, dot_size=10, gap=3)
    hd_path = "preview_senkaled_hd.png"
    img_hd.save(hd_path)
    print(f" -> Tersimpan: {hd_path} (Simulasi LED Display)")

    # 3. Render versi sample 32 C, UV 7 VERY HIGH persis seperti mockup gambar referensi
    mockup_img = render_senka_canvas(32, 7, "VERY", "HIGH", COLOR_CYAN)
    mockup_hd = create_led_matrix_simulation(mockup_img, dot_size=10, gap=3)
    mockup_path = "preview_senkaled_mockup_exact.png"
    mockup_hd.save(mockup_path)
    print(f" -> Tersimpan: {mockup_path} (Persis sesuai gambar acuan)")

    # Salin juga ke folder artifact agar bisa di-embed di laporan
    artifact_dir = r"C:\Users\USER\.gemini\antigravity\brain\df4c96da-b715-4972-82fd-243c5bf03747"
    if os.path.exists(artifact_dir):
        img_hd.save(os.path.join(artifact_dir, "preview_senkaled_hd.png"))
        mockup_hd.save(os.path.join(artifact_dir, "preview_senkaled_mockup_exact.png"))
        print(" -> File simulasi berhasil disalin ke folder artifact.")


if __name__ == "__main__":
    generate_all_previews()
