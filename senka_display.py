#!/usr/bin/env python3
"""
senka_display.py
Script Utama Eksekusi Display SenkaLed pada Raspberry Pi untuk 3 Panel P10 (96x16).
Fitur:
- Seluruh panel 2 Baris tebal (TEMP, UV IDX, UV LVL).
- Tombol Pemindah Lokasi pada GPIO 5 (Pin Fisik 29) dengan pull-up internal.
- Layar transisi otomatis (menampilkan "BLOK M" atau "CFD SUDIRMAN" selama 1.8 detik).
- Warna paten Biru Cyan Senka (COLOR_CYAN = (0, 130, 255)).
- Koreksi urutan kanal BGR untuk panel P10 fisik.
"""

import sys
import time
import signal
import threading
from display_engine import render_senka_canvas, render_location_banner, COLOR_CYAN
from weather_service import WeatherService
from wifi_manager import start_wifi_watchdog, TARGET_SSID

# Inisialisasi library hardware LED Matrix
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False
    print("[SenkaDisplay] Catatan: Modul 'rgbmatrix' tidak terdeteksi (Mode Simulasi PC).")

# Inisialisasi library tombol fisik GPIO
try:
    from gpiozero import Button
    HAS_GPIOZERO = True
except ImportError:
    HAS_GPIOZERO = False
    print("[SenkaDisplay] Catatan: Modul 'gpiozero' tidak terdeteksi (Fallback ke keyboard listener).")

# Konfigurasi Pin Tombol Ganti Lokasi
BUTTON_GPIO_PIN = 5  # Pin Fisik 29 (dihubungkan ke GND Pin 30)


def run_senka_display():
    # 0. Jalankan Wi-Fi Watchdog untuk auto-connect & auto-reconnect ke SSID modem 4G
    start_wifi_watchdog(check_interval=15)

    # 1. Jalankan Service Cuaca untuk 2 lokasi di background
    ws = WeatherService(default_location="BLOK_M", refresh_interval=600)
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
        options.drop_privileges = False # Menjaga hak akses GPIO tetap stabil
        options.led_rgb_sequence = "BGR" # Koreksi hardware panel P10 (Red & Blue terbalik)
        options.brightness = 75         # Brightness LED 75%
        # Aktifkan driver IC jika panel Anda tipe FM6127 / FM6126A:
        # options.panel_type = "FM6127"

        matrix = RGBMatrix(options=options)
        print("[SenkaDisplay] Hardware LED Matrix berhasil diinisialisasi (96x16, BGR).")
    else:
        print("[SenkaDisplay] Berjalan dalam mode simulasi / headless.")

    # Status transisi banner
    transition_lock = threading.Lock()
    in_transition = threading.Event()

    def show_transition_banner(loc_name):
        """Menampilkan banner nama lokasi selama 1.8 detik sebelum data tampil."""
        print(f"\n[SenkaDisplay] >>> BERALIH KE LOKASI: {loc_name} <<<")
        in_transition.set()
        banner_img = render_location_banner(loc_name, COLOR_CYAN)
        if matrix:
            matrix.SetImage(banner_img)
        time.sleep(1.8)
        in_transition.clear()

    def on_button_toggle():
        """Callback saat tombol GPIO 5 ditekan."""
        with transition_lock:
            new_loc_name = ws.toggle_location()
            show_transition_banner(new_loc_name)

    # 3. Setup Tombol Fisik GPIO 5 (Pin 29)
    button = None
    if HAS_GPIOZERO:
        try:
            # Menggunakan internal pull-up dan debounce 0.2 detik agar tidak double-click
            button = Button(BUTTON_GPIO_PIN, pull_up=True, bounce_time=0.2)
            button.when_pressed = on_button_toggle
            print(f"[SenkaDisplay] Tombol fisik aktif pada GPIO {BUTTON_GPIO_PIN} (Pin Fisik 29).")
        except Exception as e:
            print(f"[SenkaDisplay] Gagal inisialisasi tombol GPIO: {e}")

    # 4. Listener Keyboard (Opsional untuk pengujian via SSH tanpa tombol fisik)
    def keyboard_listener():
        while True:
            try:
                line = sys.stdin.readline()
                if line:
                    on_button_toggle()
            except Exception:
                break

    kb_thread = threading.Thread(target=keyboard_listener, daemon=True)
    kb_thread.start()
    print("[SenkaDisplay] Tips: Anda juga bisa menekan tombol [Enter] di terminal SSH untuk ganti daerah.")

    # Tangani signal exit CTRL+C dengan aman
    def signal_handler(sig, frame):
        print("\n[SenkaDisplay] Menghentikan program...")
        if matrix:
            matrix.Clear()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("[SenkaDisplay] Menampilkan data cuaca & UV...")
    # Tampilkan banner awal lokasi pertama
    init_loc = ws.get_active_location_info()["display_name"]
    show_transition_banner(init_loc)

    last_rendered_data = None

    while True:
        # Jika sedang menampilkan banner transisi, lewati render data biasa
        if in_transition.is_set():
            time.sleep(0.1)
            continue

        # Ambil data lokasi yang aktif saat ini
        current_data = ws.get_current()
        loc_id = current_data["location_id"]
        temp = current_data["temperature"]
        uv = current_data["uv_index"]
        level = current_data["uv_level"]

        # Cek apakah ada perubahan data atau lokasi
        cache_key = (loc_id, temp, uv, level)
        if cache_key != last_rendered_data and not in_transition.is_set():
            print(f"[SenkaDisplay] Update [{current_data['display_name']}]: TEMP={temp}°C | UV IDX={uv} | UV LVL={level}")
            canvas_img = render_senka_canvas(temp, uv, level, COLOR_CYAN)

            if matrix:
                matrix.SetImage(canvas_img)

            last_rendered_data = cache_key

        time.sleep(0.2)


if __name__ == "__main__":
    run_senka_display()
