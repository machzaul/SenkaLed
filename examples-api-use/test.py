#!/usr/bin/env python3

import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# 1. Konfigurasi Dasar
options = RGBMatrixOptions()

options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1

options.hardware_mapping = "regular"

# 2. MENONAKTIFKAN AUDIO (Sangat Penting untuk Pi 3B+)
# Panel LED dan audio analog menggunakan hardware clock yang sama.
# Jika audio belum dimatikan sepenuhnya di /boot/config.txt,
# baris ini wajib ditambahkan (atau tidak diberi tanda pagar).
# Jika panel berkedip parah, hidupkan baris ini.
# options.disable_hardware_pulsing = True

# 3. MENGUBAH MULTIPLEXING (Ini Adalah Solusinya)
# Ini adalah parameter yang menentukan pixel mapping.
# Untuk panel P10 1/8s, Anda harus mencoba nilai berikut SATU PER SATU.
# Silakan komentari salah satu dan aktifkan yang lain.

# Opsi A (Paling umum untuk panel outdoor 1/8s standar ABC):
#options.multiplexing = 1

# Opsi B (Juga sering digunakan untuk panel outdoor 1/8s):
	
#options.multiplexing = 4

# Opsi C (Beberapa panel P10 memerlukan ini):
#options.multiplexing = 5

# Opsi D (Gunakan 0 untuk pengujian dasar jika yang lain gagal):
options.multiplexing = 0


# 4. Inisialisasi Matrix
try:
    print("Inisialisasi matrix...")
    matrix = RGBMatrix(options=options)
except Exception as e:
    print(f"Gagal inisialisasi matrix: {e}")
    exit(1)

# 5. Membuat Gambar Uji
print("Membuat gambar uji (Garis Merah pada Kolom 0)...")
img = Image.new("RGB", (32, 16))
pix = img.load()

# Menggambar satu garis vertikal lurus pada kolom pertama (x=0)
for y in range(16):
    pix[0, y] = (255, 0, 0) # Merah solid

# 6. Menampilkan ke Panel
matrix.SetImage(img)

print("Garis merah pada kolom 0 seharusnya ditampilkan.")
print("Tekan ENTER untuk keluar...")
try:
    input() # Menunggu input user
except EOFError:
    pass # Menangani input() dari terminal

# Bersihkan matrix sebelum keluar
matrix.Clear()
print("Selesai.")
