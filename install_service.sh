#!/usr/bin/env bash
# install_service.sh
# Script otomatis untuk:
# 1. Menghapus & mematikan total service countdown lama (countdown.service)
# 2. Memasang service baru SenkaLed (senka.service) agar auto-start saat reboot

set -e

echo "=== 1. MEMATIKAN & MENGHAPUS SERVICE LAMA ==="
sudo systemctl stop countdown.service 2>/dev/null || true
sudo systemctl disable countdown.service 2>/dev/null || true
if [ -f /etc/systemd/system/countdown.service ]; then
    sudo rm -f /etc/systemd/system/countdown.service
    echo "-> File /etc/systemd/system/countdown.service berhasil dihapus permanen."
fi

echo "=== 1B. KONFIGURASI PROFIL WI-FI EVENT OTOMATIS ==="
WIFI_SSID="4G-WiFi6-2764"
WIFI_PASS="1234567890"

if command -v nmcli &> /dev/null; then
    echo "-> Mengonfigurasi Wi-Fi '$WIFI_SSID' via NetworkManager..."
    # Tambah / update koneksi agar auto-connect saat boot
    sudo nmcli connection delete "$WIFI_SSID" 2>/dev/null || true
    sudo nmcli connection add type wifi ifname wlan0 con-name "$WIFI_SSID" ssid "$WIFI_SSID" \
        wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$WIFI_PASS" \
        connection.autoconnect yes connection.autoconnect-priority 100 2>/dev/null || true
    sudo nmcli connection up "$WIFI_SSID" 2>/dev/null || true
fi

echo "=== 2. MEMBUAT SERVICE BARU (senka.service) ==="
SERVICE_FILE="/etc/systemd/system/senka.service"

sudo bash -c "cat << 'EOF' > $SERVICE_FILE
[Unit]
Description=Senka LED Matrix Weather and UV Display (96x16)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/CODX/senka/SenkaLed
ExecStart=/usr/bin/python3 /home/pi/CODX/senka/SenkaLed/senka_display.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF"

echo "-> File $SERVICE_FILE berhasil dibuat."

echo "=== 3. MENGAKTIFKAN SERVICE SENKA ==="
sudo systemctl daemon-reload
sudo systemctl enable senka.service
sudo systemctl restart senka.service

echo ""
echo "=== SELESAI! ==="
echo "Status Service Senka saat ini:"
sudo systemctl status senka.service --no-pager
