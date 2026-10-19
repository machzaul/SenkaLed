#!/usr/bin/env python3
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def uji_mapper(mux, mapper_name):
    print(f"\n---> MENGUJI MUX: {mux} | PIXEL MAPPER: {mapper_name} <---")
    
    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    
    # Ini adalah parameter kuncinya
    options.multiplexing = mux
    options.pixel_mapper_config = mapper_name
    
    try:
        matrix = RGBMatrix(options=options)
        canvas = matrix.CreateFrameCanvas()
        
        # Menggambar garis merah di kiri
        for y in range(16):
            canvas.SetPixel(0, y, 255, 0, 0)
            
        matrix.SwapOnVSync(canvas)
        time.sleep(4) # Tahan 4 detik
        
        matrix.Clear()
        del canvas
        del matrix
    except Exception as e:
        print(f"Melewati karena error: {e}")

print("=== UJI LANJUTAN: PIXEL MAPPER (ZIG-ZAG) ===")
print("Lihat panel LED. Cari garis merah lurus di sisi paling kiri.")
time.sleep(2)

# Menguji MUX dasar dengan berbagai bentuk Mapper
kombinasi_mux = [0, 1, 8]
daftar_mapper = ["U-mapper", "V-mapper", "V-mapper:Z", "Z-mapper"]

for m in kombinasi_mux:
    for map_name in daftar_mapper:
        uji_mapper(m, map_name)
        time.sleep(1)

print("\n=== SELESAI ===")
