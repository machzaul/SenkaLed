#!/usr/bin/env python3
"""
weather_service.py
Service untuk mengambil data Suhu dan UV Index Jakarta secara real-time
untuk 2 lokasi (BLOK M dan CFD SUDIRMAN) dari Open-Meteo API.
Mendukung perpindahan lokasi dinamis via tombol fisik, offline caching terpisah,
dan format kategori UV ringkas (LOW, MED, HIGH, VHI, EXT).
"""

import json
import os
import time
import threading
import requests

# Konfigurasi 2 Lokasi Pemantauan Jakarta
LOCATIONS = {
    "BLOK_M": {
        "id": "BLOK_M",
        "display_name": "BLOK M",
        "full_name": "Kawasan Blok M, Jakarta Selatan",
        "lat": -6.244342,
        "lon": 106.799238,
        "cache_file": os.path.join(os.path.dirname(__file__), "weather_cache_blokm.json")
    },
    "CFD": {
        "id": "CFD",
        "display_name": "CFD SUDIRMAN",
        "full_name": "Koridor CFD Sudirman / Senayan, Jakarta",
        "lat": -6.224413,
        "lon": 106.803868,
        "cache_file": os.path.join(os.path.dirname(__file__), "weather_cache_cfd.json")
    }
}


def get_uv_short_level(uv_value):
    """
    Mengonversi nilai numerik UV ke kategori level standar:
    - 0 - 2.9 : LOW
    - 3 - 5.9 : MED
    - 6 - 10.9: HIGH (Tinggi)
    - 11+     : EXT (Ekstrem)
    """
    if uv_value < 3.0:
        return "LOW"
    elif uv_value < 6.0:
        return "MED"
    elif uv_value < 11.0:
        return "HIGH"
    else:
        return "EXT"


class WeatherService:
    def __init__(self, default_location="BLOK_M", refresh_interval=600, retry_interval=30):
        self.active_location_id = default_location
        self.refresh_interval = refresh_interval  # 10 menit saat online normal
        self.retry_interval = retry_interval      # 30 detik saat koneksi internet putus
        self.lock = threading.Lock()
        
        # Penyimpanan data untuk masing-masing lokasi
        self.location_data = {}
        for loc_id, cfg in LOCATIONS.items():
            self.location_data[loc_id] = {
                "location_id": loc_id,
                "display_name": cfg["display_name"],
                "temperature": 32,
                "uv_index": 7,
                "uv_level": "HIGH",
                "last_updated": 0,
                "status": "initial_default"
            }
            # Muat cache per lokasi jika ada
            self._load_cache(loc_id)

    def _load_cache(self, loc_id):
        cfg = LOCATIONS[loc_id]
        cache_path = cfg["cache_file"]
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    cached = json.load(f)
                    with self.lock:
                        self.location_data[loc_id].update(cached)
                        self.location_data[loc_id]["status"] = "offline_cache"
                print(f"[WeatherService] Cache dimuat ({cfg['display_name']}): {self.location_data[loc_id]['temperature']}°C, UV {self.location_data[loc_id]['uv_index']} ({self.location_data[loc_id]['uv_level']})")
            except Exception as e:
                print(f"[WeatherService] Gagal memuat cache {loc_id}: {e}")

    def _save_cache(self, loc_id):
        cfg = LOCATIONS[loc_id]
        cache_path = cfg["cache_file"]
        try:
            with open(cache_path, "w") as f:
                with self.lock:
                    json.dump(self.location_data[loc_id], f, indent=2)
        except Exception as e:
            print(f"[WeatherService] Gagal menyimpan cache {loc_id}: {e}")

    def fetch_data_for(self, loc_id):
        """Mengambil data real-time dari API Open-Meteo untuk lokasi tertentu."""
        cfg = LOCATIONS.get(loc_id)
        if not cfg:
            return False

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={cfg['lat']}&longitude={cfg['lon']}&"
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
                level_str = get_uv_short_level(raw_uv)

                with self.lock:
                    self.location_data[loc_id] = {
                        "location_id": loc_id,
                        "display_name": cfg["display_name"],
                        "temperature": temp_int,
                        "uv_index": uv_int,
                        "uv_level": level_str,
                        "last_updated": time.time(),
                        "status": "online"
                    }
                self._save_cache(loc_id)
                print(f"[WeatherService][ONLINE] {cfg['display_name']} -> {temp_int}°C, UV {uv_int} ({level_str})")
                return True
        except Exception as e:
            with self.lock:
                self.location_data[loc_id]["status"] = "offline"
            print(f"[WeatherService][OFFLINE] Gagal fetch {cfg['display_name']}: {e}. Memakai cache.")
        return False

    def fetch_all(self):
        """Mengambil data untuk semua lokasi yang terdaftar."""
        ok = True
        for loc_id in LOCATIONS.keys():
            if not self.fetch_data_for(loc_id):
                ok = False
        return ok

    def toggle_location(self):
        """Beralih ke lokasi berikutnya (BLOK M <-> CFD SUDIRMAN)."""
        with self.lock:
            if self.active_location_id == "BLOK_M":
                self.active_location_id = "CFD"
            else:
                self.active_location_id = "BLOK_M"
            target_info = LOCATIONS[self.active_location_id]
            print(f"[WeatherService] Lokasi aktif beralih ke: {target_info['display_name']}")
            return target_info["display_name"]

    def set_location(self, loc_id):
        if loc_id in LOCATIONS:
            with self.lock:
                self.active_location_id = loc_id
                return LOCATIONS[loc_id]["display_name"]
        return None

    def get_active_location_info(self):
        with self.lock:
            return LOCATIONS[self.active_location_id]

    def get_current(self):
        """Mengembalikan data lokasi yang sedang aktif saat ini."""
        with self.lock:
            return dict(self.location_data[self.active_location_id])

    def start_background_updater(self):
        """Menjalankan loop auto-refresh di background thread."""
        def worker():
            success = self.fetch_all()
            while True:
                sleep_time = self.refresh_interval if success else self.retry_interval
                time.sleep(sleep_time)
                success = self.fetch_all()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread


if __name__ == "__main__":
    ws = WeatherService()
    print("Testing manual fetch untuk semua lokasi:")
    ws.fetch_all()
    print("Current active location data:", ws.get_current())
    print("\nToggle location...")
    ws.toggle_location()
    print("Current active location data:", ws.get_current())
