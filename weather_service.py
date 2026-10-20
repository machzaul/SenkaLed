#!/usr/bin/env python3
"""
weather_service.py
Service untuk mengambil data Suhu dan UV Index Jakarta secara real-time
dari Open-Meteo API dengan sistem offline caching dan background auto-refresh.
"""

import json
import os
import time
import threading
import requests

# Koordinat lokasi Jakarta (area FX Sudirman / Senayan / SCBD)
DEFAULT_LAT = -6.224413119718039
DEFAULT_LON = 106.80386768026403

CACHE_FILE = os.path.join(os.path.dirname(__file__), "weather_cache.json")


def get_uv_scale(uv_value):
    """
    Mengonversi nilai numerik UV ke kategori skala WHO (2 baris teks).
    """
    if uv_value < 3.0:
        return ("UV", "LOW")
    elif uv_value < 6.0:
        return ("MED-", "IUM")
    elif uv_value < 8.0:
        return ("UV", "HIGH")
    elif uv_value < 11.0:
        return ("VERY", "HIGH")
    else:
        return ("EXT-", "REME")


class WeatherService:
    def __init__(self, lat=DEFAULT_LAT, lon=DEFAULT_LON, refresh_interval=600):
        self.lat = lat
        self.lon = lon
        self.refresh_interval = refresh_interval  # 10 menit (600 detik)
        self.lock = threading.Lock()
        
        # Nilai default awal jika belum ada koneksi sama sekali
        self.data = {
            "temperature": 32,
            "uv_index": 7,
            "uv_line1": "VERY",
            "uv_line2": "HIGH",
            "last_updated": 0,
            "status": "initial"
        }
        
        # Load data dari cache lokal jika file tersedia
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    cached = json.load(f)
                    with self.lock:
                        self.data.update(cached)
            except Exception as e:
                print(f"[WeatherService] Gagal memuat cache: {e}")

    def _save_cache(self):
        try:
            with open(CACHE_FILE, "w") as f:
                with self.lock:
                    json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"[WeatherService] Gagal menyimpan cache: {e}")

    def fetch_data(self):
        """
        Mengambil data real-time langsung dari Open-Meteo API.
        """
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.lat}&longitude={self.lon}&"
            f"current=temperature_2m,uv_index&timezone=Asia%2FJakarta"
        )
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                payload = res.json()
                current = payload.get("current", {})
                raw_temp = current.get("temperature_2m", 32.0)
                raw_uv = current.get("uv_index", 7.0)

                temp_int = int(round(raw_temp))
                uv_int = int(round(raw_uv))
                line1, line2 = get_uv_scale(raw_uv)

                with self.lock:
                    self.data = {
                        "temperature": temp_int,
                        "uv_index": uv_int,
                        "uv_line1": line1,
                        "uv_line2": line2,
                        "last_updated": time.time(),
                        "status": "online"
                    }
                self._save_cache()
                print(f"[WeatherService] Data berhasil diperbarui: {temp_int}°C, UV {uv_int} ({line1} {line2})")
                return True
            else:
                print(f"[WeatherService] API error code: {res.status_code}")
        except Exception as e:
            print(f"[WeatherService] Gagal mengambil data cuaca: {e}. Menggunakan cache terakhir.")
        return False

    def get_current(self):
        """
        Mengembalikan data cuaca terkini yang aman diakses dari thread manapun.
        """
        with self.lock:
            return dict(self.data)

    def start_background_updater(self):
        """
        Menjalankan loop background thread untuk auto-refresh data secara berkala.
        """
        def worker():
            # Coba fetch pertama kali saat start
            self.fetch_data()
            while True:
                time.sleep(self.refresh_interval)
                self.fetch_data()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread


if __name__ == "__main__":
    service = WeatherService()
    print("Testing manual fetch:")
    service.fetch_data()
    print("Current data:", service.get_current())
