import os
import time
import threading
import subprocess
from panel import create_panel
from digital_font import DigitalFont
from gpiozero import Button

print(f"[DEBUG] UID sebelum create_panel: real={os.getuid()} effective={os.geteuid()}")
matrix = create_panel()
print(f"[DEBUG] UID sesudah create_panel: real={os.getuid()} effective={os.geteuid()}")

font = DigitalFont()
RED = (255, 0, 0)
YELLOW = (255, 200, 0)

# ==================================================
# REFLECTION GAME
# hitung naik 00:00 -> 99:99 (lalu ulang lagi)
# target: tekan tombol AKSI tepat di 15:00
#
# KONTROL:
#   Tombol fisik (GPIO):
#     - GPIO5  (pin fisik 29) -> ganti mode tampilan (SS:MS <-> SS:CS:MC)
#     - GPIO6  (pin fisik 31) -> aksi (mulai hitung mundur ulang / catat tekanan)
#     kedua tombol dipasang antara pin GPIO dan GND terdekat,
#     memakai pull-up internal (pull_up=True) jadi tidak perlu resistor luar.
#   Keyboard (fallback untuk testing tanpa tombol fisik):
#     - a + Enter -> sama seperti tombol mode
#     - b + Enter -> sama seperti tombol aksi
# ==================================================
TARGET_SEC = 15
TARGET_CENTI = 0

# mode tampilan: "2" = SS:MS (font besar), "3" = SS:CS:MC (font kecil)
display_mode = "2"

COUNTDOWN_MAX_WAIT = 8  # detik

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, "Audio")

SOUND_WIN = os.path.join(AUDIO_DIR, "win.mp3")
SOUND_WRONG = os.path.join(AUDIO_DIR, "wrong.mp3")
SOUND_COUNTDOWN = os.path.join(AUDIO_DIR, "countdown.mp3")

AUDIO_DEVICE = "plughw:1,0"

# ganti kalau kamu pasang tombol di GPIO lain
BUTTON_MODE_GPIO = 5    # pin fisik 29 -> ganti mode tampilan
BUTTON_ACTION_GPIO = 6  # pin fisik 31 -> aksi


def _audio_env():
    env = os.environ.copy()
    env["HOME"] = "/tmp"
    return env


def play_sound(path):
    try:
        subprocess.Popen(
            ["mpg123", "-q", "-o", "alsa", "-a", AUDIO_DEVICE, path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            env=_audio_env(),
        )
    except Exception as e:
        print(f"[AUDIO ERROR] Gagal memutar {path}: {e}")


def play_music_tracked(path):
    try:
        proc = subprocess.Popen(
            ["mpg123", "-q", "-o", "alsa", "-a", AUDIO_DEVICE, path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            env=_audio_env(),
        )
        print(f"[DEBUG] mpg123 dijalankan, PID={proc.pid}, file={path}")
        return proc
    except Exception as e:
        print(f"[AUDIO ERROR] Gagal memutar {path}: {e}")
        return None


def draw_current(sec, centi, micro, color):
    # gambar sesuai mode tampilan yang aktif saat ini
    font.clear()
    if display_mode == "2":
        font.draw_time(sec, centi, color)
    else:
        font.draw_time_micro(sec, centi, micro, color)
    matrix.SetImage(font.get_image())


running = True
enter_event = threading.Event()  # di-set oleh tombol aksi (GPIO6 atau 'b')


def toggle_mode():
    global display_mode
    display_mode = "3" if display_mode == "2" else "2"
    label = "SS:CS:MC (3 grup)" if display_mode == "3" else "SS:MS (2 grup)"
    print(f"[DEBUG] mode tampilan diganti -> {label}")


def trigger_action():
    print("[DEBUG] tombol aksi terdeteksi")
    enter_event.set()


# ==================================================
# TOMBOL FISIK (GPIO)
# pull_up=True -> pin default HIGH, saat ditekan (terhubung ke GND) jadi LOW
# bounce_time -> debounce software, supaya satu tekanan tidak terbaca berkali-kali
# ==================================================
btn_mode = Button(BUTTON_MODE_GPIO, pull_up=True, bounce_time=0.05)
btn_action = Button(BUTTON_ACTION_GPIO, pull_up=True, bounce_time=0.05)

btn_mode.when_pressed = toggle_mode
btn_action.when_pressed = trigger_action


def input_listener():
    # fallback keyboard, tetap aktif buat testing tanpa tombol fisik.
    # baca satu baris teks: "a" untuk ganti mode, "b" untuk aksi.
    while running:
        try:
            line = input()
        except EOFError:
            break

        cmd = line.strip().lower()

        if cmd == "a":
            toggle_mode()
        elif cmd == "b":
            trigger_action()
        else:
            print(f"[DEBUG] input '{line}' diabaikan (pakai 'a' untuk ganti mode, 'b' untuk aksi)")


listener = threading.Thread(target=input_listener, daemon=True)
listener.start()

print("Bersiap... memutar musik countdown")
print(f"Kontrol: tombol GPIO{BUTTON_MODE_GPIO} = ganti mode, GPIO{BUTTON_ACTION_GPIO} = aksi "
      "(atau ketik 'a'/'b' + Enter di keyboard).")

# RUNNING    = hitung jalan
# STOPPED    = menampilkan hasil, nunggu tombol aksi
# COUNTDOWN  = musik countdown.mp3 diputar, nunggu sampai selesai
#              baru pindah ke RUNNING
state = "COUNTDOWN"
start = time.time()
sec = 0
centi = 0
micro = 0

# mulai main -> putar countdown.mp3 dulu sebelum hitungan jalan
countdown_proc = play_music_tracked(SOUND_COUNTDOWN)
countdown_wait_start = time.time()

try:
    while True:
        if state == "RUNNING":
            elapsed = time.time() - start
            # total_units dalam satuan 1/10000 detik -> wrap tiap 100 detik
            total_units = int(elapsed * 10000) % 1000000
            sec = (total_units // 10000) % 100
            centi = (total_units // 100) % 100
            micro = total_units % 100  # sub-digit presisi lebih (satuan 100 mikrodetik)

            draw_current(sec, centi, micro, RED)

            if enter_event.is_set():
                enter_event.clear()
                if sec == TARGET_SEC and centi == TARGET_CENTI:
                    print(f"[LOG] BERHASIL! Tepat di {sec:02d}:{centi:02d}")
                    play_sound(SOUND_WIN)
                else:
                    print(f"[LOG] GAGAL! Kamu menekan di {sec:02d}:{centi:02d} "
                          f"(target {TARGET_SEC:02d}:{TARGET_CENTI:02d})")
                    play_sound(SOUND_WRONG)
                # panel berhenti, tetap tampilkan angka terakhir
                state = "STOPPED"
                print("[DEBUG] state -> STOPPED")

        elif state == "STOPPED":
            # panel diam menampilkan hasil terakhir,
            # menunggu tombol aksi berikutnya untuk mulai countdown
            if enter_event.is_set():
                enter_event.clear()
                print("[DEBUG] STOPPED -> mulai COUNTDOWN lagi")
                draw_current(0, 0, 0, YELLOW)
                countdown_proc = play_music_tracked(SOUND_COUNTDOWN)
                countdown_wait_start = time.time()
                state = "COUNTDOWN"

        else:  # COUNTDOWN
            # abaikan tombol aksi yang ditekan selagi musik countdown main
            if enter_event.is_set():
                enter_event.clear()
                print("[DEBUG] tombol aksi diabaikan (masih COUNTDOWN)")

            music_done = (countdown_proc is None) or (countdown_proc.poll() is not None)
            timed_out = (time.time() - countdown_wait_start) >= COUNTDOWN_MAX_WAIT

            if music_done or timed_out:
                if timed_out and not music_done:
                    print(f"[WARNING] Musik countdown belum selesai setelah "
                          f"{COUNTDOWN_MAX_WAIT} detik, lanjut hitung tanpa nunggu lagi.")
                elif countdown_proc is not None:
                    rc = countdown_proc.returncode
                    if rc != 0:
                        print(f"[AUDIO ERROR] mpg123 keluar dengan kode error {rc} "
                              f"(bukan 0 = normal). Kemungkinan device/format audio bermasalah.")
                # musik countdown sudah selesai (atau kelamaan) -> mulai hitung
                start = time.time()
                state = "RUNNING"
                print("[DEBUG] state -> RUNNING")

        time.sleep(0.01)

except KeyboardInterrupt:
    running = False
    print("\nGame dihentikan.")
