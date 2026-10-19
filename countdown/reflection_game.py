import time
import threading
from digital_font import DigitalFont

# ==================================================
# REFLECTION GAME
# Panel hitung dari 00:00 -> 99:99 (lalu ulang lagi)
# Target: tekan ENTER TEPAT di 15:00
# ==================================================

TARGET_SEC   = 15
TARGET_CENTI = 0

COLOR = (255, 0, 0)


class ReflectionGame:
    def __init__(self):
        self.font = DigitalFont()
        self.running = True

        self.sec = 0
        self.centi = 0
        self._start_time = time.time()

        # dipakai untuk komunikasi antar thread (tombol vs loop utama)
        self._enter_event = threading.Event()

    # --------------------------------------------
    # RESET WAKTU KE 00:00
    # --------------------------------------------
    def reset(self):
        self._start_time = time.time()
        self.sec = 0
        self.centi = 0

    # --------------------------------------------
    # UPDATE WAKTU BERJALAN
    # dari 00:00 sampai 99:99, lalu balik lagi ke 00:00
    # --------------------------------------------
    def update(self):
        elapsed = time.time() - self._start_time
        total_centi = int(elapsed * 100) % 10000
        self.sec = total_centi // 100
        self.centi = total_centi % 100

    # --------------------------------------------
    # RENDER KE PANEL (ATAU PREVIEW)
    # ganti/lengkapi bagian ini nanti dengan kode
    # pengiriman frame ke panel P10 fisik
    # --------------------------------------------
    def render(self):
        self.font.clear()
        self.font.draw_time(self.sec, self.centi, COLOR)
        frame = self.font.get_image()
        # TODO: kirim `frame` ke driver panel P10 di sini
        return frame

    # --------------------------------------------
    # CEK HASIL SAAT ENTER DITEKAN
    # --------------------------------------------
    def check_press(self):
        if self.sec == TARGET_SEC and self.centi == TARGET_CENTI:
            print(f"[LOG] BERHASIL!  Tepat di {self.sec:02d}:{self.centi:02d}")
        else:
            print(f"[LOG] GAGAL!  Kamu menekan di {self.sec:02d}:{self.centi:02d} "
                  f"(target {TARGET_SEC:02d}:{TARGET_CENTI:02d})")
        self.reset()

    # --------------------------------------------
    # SINYAL DARI THREAD INPUT
    # --------------------------------------------
    def trigger_enter(self):
        self._enter_event.set()

    def consume_enter(self):
        if self._enter_event.is_set():
            self._enter_event.clear()
            return True
        return False


def input_listener(game: ReflectionGame):
    """
    Thread terpisah supaya menunggu ENTER tidak
    memblokir update tampilan waktu di loop utama.
    Nantinya bagian ini bisa diganti dengan pembacaan
    tombol fisik (GPIO) tanpa mengubah logika game.
    """
    while game.running:
        try:
            input()
        except EOFError:
            break
        game.trigger_enter()


def main():
    game = ReflectionGame()

    listener = threading.Thread(target=input_listener, args=(game,), daemon=True)
    listener.start()

    print("==============================================")
    print(" REFLECTION GAME")
    print(f" Tekan ENTER tepat saat panel menunjukkan "
          f"{TARGET_SEC:02d}:{TARGET_CENTI:02d}")
    print(" Tekan Ctrl+C untuk keluar")
    print("==============================================")

    try:
        while True:
            game.update()
            game.render()

            # tampilkan waktu berjalan di terminal
            print(f"\r{game.sec:02d} : {game.centi:02d}   ", end="", flush=True)

            if game.consume_enter():
                print()  # pindah baris sebelum log
                game.check_press()

            time.sleep(0.01)

    except KeyboardInterrupt:
        game.running = False
        print("\nGame dihentikan.")


if __name__ == "__main__":
    main()
