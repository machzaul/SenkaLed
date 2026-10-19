#!/usr/bin/env python3
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def uji_multiplexing(nilai_mux):
    print(f"\n---> MENGUJI MULTIPLEXING: {nilai_mux} <---")
    print("Lihat panel LED Anda sekarang!")
    
    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    
    # Memasukkan nilai multiplexing yang sedang diuji
    options.multiplexing = nilai_mux
    
    try:
        # Inisialisasi panel
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        
        # Menggambar garis merah di kolom paling kiri (X = 0)
        # dan garis hijau di kolom paling kanan (X = 31) sebagai batas
        for y in range(16):
            canvas.SetPixel(0, y, 255, 0, 0)   # Merah di kiri
            canvas.SetPixel(31, y, 0, 255, 0)  # Hijau di kanan
            
        matrix.SwapOnVSync(canvas)
        
        # Tahan selama 4 detik agar Anda punya waktu untuk melihat
        time.sleep(4)
        
        # Bersihkan memori agar bisa memulai ulang untuk angka berikutnya
        matrix.Clear()
        del canvas
        del matrix
        
    except Exception as e:
        print(f"Gagal memuat multiplexing {nilai_mux}. Error: {e}")

# Memulai proses pengujian dari angka 0 sampai 17
print("=== MEMULAI PENGUJIAN OTOMATIS ===")
print("Catat angka di layar ini saat panel menunjukkan GARIS LURUS SEMPURNA.")
print("Dimulai dalam 3 detik...\n")
time.sleep(3)

for mux in range(18):
    uji_multiplexing(mux)
    time.sleep(1) # Jeda 1 detik sebelum angka berikutnya

print("\n=== PENGUJIAN SELESAI ===")
print("Apakah Anda menemukan angka yang membuat garis merah lurus sempurna di kiri?")
