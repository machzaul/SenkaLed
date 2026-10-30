#!/usr/bin/env python3
"""
wifi_manager.py
Modul pengelola koneksi Wi-Fi otomatis untuk Raspberry Pi (Debian Bookworm/Bullseye).
- Menghubungkan secara otomatis ke SSID target (misal: modem 4G event)
- Background auto-reconnect jika koneksi terputus
- Mendukung NetworkManager (nmcli) dan wpa_supplicant
"""

import subprocess
import time
import threading

# Konfigurasi Wi-Fi Target (dari modem 4G booth event)
TARGET_SSID = "4G-WiFi6-2764"
TARGET_PSK = "1234567890"


def check_internet():
    """Memeriksa apakah Raspberry Pi memiliki akses internet riil."""
    try:
        # Coba ping DNS Google atau request ringan
        res = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return res.returncode == 0
    except Exception:
        return False


def get_current_wifi_ssid():
    """Mendapatkan nama SSID yang sedang terhubung saat ini."""
    # 1. Coba lewat nmcli (NetworkManager - default di Raspberry Pi OS Bookworm)
    try:
        res = subprocess.run(
            ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if res.returncode == 0:
            for line in res.stdout.strip().split("\n"):
                if line.startswith("yes:"):
                    return line.split(":", 1)[1]
    except Exception:
        pass

    # 2. Coba lewat iwgetid
    try:
        res = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass

    return None


def connect_to_target_wifi(ssid=TARGET_SSID, psk=TARGET_PSK):
    """Menghubungkan ke Wi-Fi target menggunakan nmcli atau wpa_cli."""
    print(f"[WiFiManager] Memeriksa & menghubungkan ke Wi-Fi: '{ssid}'...")
    
    # 1. Gunakan nmcli jika tersedia (NetworkManager)
    try:
        cmd = ["nmcli", "dev", "wifi", "connect", ssid, "password", psk]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            print(f"[WiFiManager] Berhasil terhubung ke '{ssid}' via NetworkManager.")
            return True
        else:
            msg = res.stderr.strip() or res.stdout.strip()
            # Jika sudah aktif atau profil sudah ada
            if "already active" in msg.lower() or "activated" in msg.lower():
                print(f"[WiFiManager] Koneksi '{ssid}' aktif.")
                return True
            print(f"[WiFiManager] nmcli info: {msg}")
    except Exception as e:
        print(f"[WiFiManager] nmcli error: {e}")

    # 2. Fallback jika memakai wpa_cli / raspi-config
    try:
        cmd = ["wpa_cli", "-i", "wlan0", "reassociate"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
    except Exception:
        pass

    return False


def start_wifi_watchdog(ssid=TARGET_SSID, psk=TARGET_PSK, check_interval=15):
    """
    Menjalankan background thread pemantau Wi-Fi.
    Jika Wi-Fi terputus atau tidak terhubung ke target, akan auto-reconnect tiap check_interval detik.
    """
    def watchdog_worker():
        print(f"[WiFiManager] Watchdog aktif untuk Wi-Fi '{ssid}'.")
        # Saat pertama kali start, cek apakah sudah tersambung
        time.sleep(2)
        curr = get_current_wifi_ssid()
        if curr != ssid:
            connect_to_target_wifi(ssid, psk)

        while True:
            time.sleep(check_interval)
            curr = get_current_wifi_ssid()
            has_internet = check_internet()

            # Jika Wi-Fi lepas ATAU internet tidak bisa diakses
            if curr != ssid or not has_internet:
                print(f"[WiFiManager][WARNING] Wi-Fi terputus / belum terhubung ke '{ssid}' (Current: {curr}). Menghubungkan ulang...")
                connect_to_target_wifi(ssid, psk)

    thread = threading.Thread(target=watchdog_worker, daemon=True)
    thread.start()
    return thread


if __name__ == "__main__":
    print(f"Current Wi-Fi: {get_current_wifi_ssid()}")
    print(f"Internet OK: {check_internet()}")
    connect_to_target_wifi()
