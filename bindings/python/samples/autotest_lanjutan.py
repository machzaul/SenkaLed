#!/usr/bin/env python3
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def uji_kombinasi(mux, addr_type):
    print(f"\n---> MENGUJI MUX: {mux} | ROW_ADDRESS_TYPE: {addr_type} <---")

    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"

    # Perbaikan nama atribut di sini:
    options.multiplexing = mux
    options.row_address_type = addr_type

    try:
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()

        # Gambar garis merah di kiri
        for y in range(16):
            canvas.SetPixel(0, y, 255, 0, 0)

        matrix.SwapOnVSync(canvas)
        time.sleep(3) # Tahan 3 detik

        matrix.Clear()
        del canvas
        del matrix
    except Exception as e:
        print(f"Melewati kombinasi karena error internal: {e}")

print("=== UJI LANJUTAN: TIPE PENGALAMATAN ===")
print("Lihat layar panel LED. Cari garis merah lurus di sisi paling kiri.")
time.sleep(2)

# Menguji mux P10 yang paling umum dengan 4 tipe row_address_type
kombinasi_mux = [0, 1, 4, 8, 9]
kombinasi_addr = [1, 2, 3, 4]

for m in kombinasi_mux:
    for a in kombinasi_addr:
        uji_kombinasi(m, a)
        time.sleep(1)

print("\n=== SELESAI ===")
