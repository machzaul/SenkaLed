#!/usr/bin/env python3
"""
senka_display.py
Script Utama Eksekusi Display SenkaLed pada Raspberry Pi untuk 3 Panel P10 (96x16).
Warna: Biru Cyan Langit #27CCF5.
Update Data: Real-time background fetch dari Open-Meteo API (Jakarta) tiap 10 menit.
"""

import sys
import time
import signal
from display_engine import render_senka_canvas, COLOR_BLUE
from weather_service import WeatherService

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False
    print("[SenkaDisplay] Catatan: Modul 'rgbmatrix' tidak terdeteksi (Mode Simulasi PC).")


def run_senka_display():
    # 1. Jalankan Service Cuaca Jakarta di background
    ws = WeatherService(refresh_interval=600)  # Refresh tiap 10 menit
    ws.start_background_updater()

    # 2. Inisialisasi Hardware LED Matrix (jika di Raspberry Pi)
    matrix = None
    if HAS_HARDWARE:
        options = RGBMatrixOptions()
        options.rows = 16
        options.cols = 32
        options.chain_length = 3        # 3 Panel P10 disambung serial (Total 96x16)
        options.parallel = 1
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 2       # Standar stabil Raspberry Pi 3/4
        options.drop_privileges = False # Sesuai konfigurasi panel.py program sebelumnya
        options.led_rgb_sequence = "BGR" # Koreksi hardware panel P10 (Red & Blue terbalik)
        options.brightness = 75         # Brightness LED 75%
        # Aktifkan driver IC jika panel Anda tipe FM6127 / FM6126A:
        # options.panel_type = "FM6127"

        matrix = RGBMatrix(options=options)
        print("[SenkaDisplay] Hardware LED Matrix berhasil diinisialisasi (96x16).")
    else:
        print("[SenkaDisplay] Berjalan dalam mode headless / test.")

    # Tangani signal exit CTRL+C dengan aman
    def signal_handler(sig, frame):
        print("\n[SenkaDisplay] Menghentikan program...")
        if matrix:
            matrix.Clear()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("[SenkaDisplay] Layar Senka aktif. Menampilkan Suhu & UV Index Jakarta...")

    last_rendered_data = None

    while True:
        # Dapatkan data cuaca terkini
        current_data = ws.get_current()
        temp = current_data["temperature"]
        uv = current_data["uv_index"]
        line1 = current_data["uv_line1"]
        line2 = current_data["uv_line2"]

        # Cek apakah ada perubahan data
        cache_key = (temp, uv, line1, line2)
        if cache_key != last_rendered_data:
            print(f"[SenkaDisplay] Update tampilan: {temp}°C | UV {uv} | {line1} {line2}")
            # Render kanvas 96x16 dengan warna Biru Murni (0, 0, 255)
            canvas_img = render_senka_canvas(temp, uv, line1, line2, COLOR_BLUE)

            if matrix:
                matrix.SetImage(canvas_img)

            last_rendered_data = cache_key

        time.sleep(1)


if __name__ == "__main__":
    run_senka_display()
