#!/usr/bin/env python
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# 1. Konfigurasi Panel (Sesuai dengan demo Anda)
options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.multiplexing = 3
# options.disable_hardware_pulsing = True # Hapus tanda pagar di depan baris ini jika masih ada error suara

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()

# 2. Memuat Font bawaan
# Menggunakan font 5x8 karena ukurannya pas untuk panel 32 pixel
font = graphics.Font()
font.LoadFont("../../../fonts/5x8.bdf") 

# Warna Teks (Merah)
textColor = graphics.Color(255, 0, 0)

# 3. Logika Hitung Mundur 15 Detik
waktu_mulai = time.time()
durasi = 15.0

while True:
    waktu_sekarang = time.time()
    waktu_berlalu = waktu_sekarang - waktu_mulai
    waktu_tersisa = durasi - waktu_berlalu

    # Hentikan waktu di angka 0 agar tidak minus
    if waktu_tersisa <= 0:
        waktu_tersisa = 0

    # Memisahkan detik dan pecahan detik (centisecond)
    detik = int(waktu_tersisa)
    # Diambil 2 digit di belakang koma agar muat di layar 32 pixel
    milidetik = int((waktu_tersisa - detik) * 100) 

    # Format teks: "15:99" menjadi "00:00"
    teks = f"{detik:02d}:{milidetik:02d}"

    # Bersihkan layar sebelum menggambar teks baru
    canvas.Clear()
    
    # Menggambar teks (posisi X=2, Y=12 agar posisinya di tengah panel)
    graphics.DrawText(canvas, font, 2, 12, textColor, teks)
    
    # Render ke panel LED
    canvas = matrix.SwapOnVSync(canvas)

    # Jika waktu sudah habis, tahan angka 00:00 selama 3 detik lalu keluar
    if waktu_tersisa == 0:
        time.sleep(3)
        break
        
# Matikan panel saat program selesai
matrix.Clear()

