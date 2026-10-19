import os
import time
import threading
import subprocess
from panel import create_panel
from digital_font import DigitalFont

# [DEBUG] cek UID sebelum panel diinisialisasi (harus 0 = root, karena dijalankan via sudo)
print(f"[DEBUG] UID sebelum create_panel: real={os.getuid()} effective={os.geteuid()}")
matrix = create_panel()
# [DEBUG] cek UID sesudah panel diinisialisasi
# rgbmatrix drop privileges dari root ke user biasa setelah GPIO/mem siap,
# kalau angka di bawah ini beda dari yang di atas, itu konfirmasi penyebab masalah audio
print(f"[DEBUG] UID sesudah create_panel: real={os.getuid()} effective={os.geteuid()}")

font = DigitalFont()
RED = (255, 0, 0)
YELLOW = (255, 200, 0)

# ==================================================
# REFLECTION GAME
# hitung naik 00:00 -> 99:99 (lalu ulang lagi)
# target: tekan ENTER tepat di 15:00
# ==================================================
TARGET_SEC = 15
TARGET_CENTI = 0

# batas maksimal nunggu musik countdown, sebagai pengaman
# supaya game tidak macet total kalau file kepanjangan
# atau device audio bermasalah
COUNTDOWN_MAX_WAIT = 8  # detik (file countdown.mp3 Anda ~5 detik, beri buffer aman)

# folder Audio/ selalu dicari relatif terhadap lokasi
# script ini sendiri, bukan working directory saat dijalankan
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(SCRIPT_DIR, "Audio")

SOUND_WIN = os.path.join(AUDIO_DIR, "win.mp3")
SOUND_WRONG = os.path.join(AUDIO_DIR, "wrong.mp3")
SOUND_COUNTDOWN = os.path.join(AUDIO_DIR, "countdown.mp3")

# device audio USB Anda: card 1, device 0 (dari hasil "sudo aplay -l")
# dengan device eksplisit, mpg123 tidak perlu lagi mencoba-coba
# puluhan kombinasi device otomatis (sysdefault/hdmi/dmix/pulse/dst)
# yang selama ini bikin lambat & gagal saat dipanggil dari Python
AUDIO_DEVICE = "plughw:1,0"

# ganti "pi" di bawah ini kalau user login kamu bukan "pi"
AUDIO_USER = "pi"


def _audio_env():
    # <-- FIX: setelah create_panel(), proses ini sudah di-drop dari root
    # ke user biasa (pi) oleh library rgbmatrix, tapi $HOME masih
    # ke-inherit dari sesi sudo awal (/root). Kita perbaiki di sini
    # supaya mpg123 tidak coba menulis ke /root/.config/pulse,
    # yang tidak lagi ia punya izin akses setelah privilege drop.
    env = os.environ.copy()
    env["HOME"] = os.path.expanduser(f"~{AUDIO_USER}")
    return env


def play_sound(path):
    # non-blocking, dipakai untuk win/wrong (tidak perlu ditunggu)
    # stdin=DEVNULL supaya mpg123 tidak rebutan baca keyboard
    # dengan input_listener() kita.
    # stderr TIDAK dibungkam supaya kalau ada masalah device
    # audio (mis. saat jalan via sudo), pesannya kelihatan di
    # terminal, bukan disembunyikan diam-diam.
    try:
        subprocess.Popen(
            ["mpg123", "-q", "-o", "alsa", "-a", AUDIO_DEVICE, path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            env=_audio_env(),  # <-- FIX
        )
    except Exception as e:
        print(f"[AUDIO ERROR] Gagal memutar {path}: {e}")


def play_music_tracked(path):
    # sama seperti play_sound, tapi process handle-nya
    # dikembalikan supaya bisa dicek kapan selesai
    try:
        proc = subprocess.Popen(
            ["mpg123", "-q", "-o", "alsa", "-a", AUDIO_DEVICE, path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            env=_audio_env(),  # <-- FIX
        )
        print(f"[DEBUG] mpg123 dijalankan, PID={proc.pid}, file={path}")
        return proc
    except Exception as e:
        print(f"[AUDIO ERROR] Gagal memutar {path}: {e}")
        return None


running = True
enter_event = threading.Event()


def input_listener():
    # thread terpisah supaya menunggu ENTER
    # tidak menghentikan update panel
    # nanti bisa diganti pembacaan tombol fisik (GPIO)
    while running:
        try:
            input()
        except EOFError:
            break
        print("[DEBUG] ENTER terdeteksi oleh input_listener")
        enter_event.set()


listener = threading.Thread(target=input_listener, daemon=True)
listener.start()

print("Bersiap... memutar musik countdown")

# RUNNING    = hitung jalan
# STOPPED    = menampilkan hasil, nunggu ENTER
# COUNTDOWN  = musik countdown.mp3 diputar, nunggu sampai selesai
#              baru pindah ke RUNNING
state = "COUNTDOWN"
start = time.time()
sec = 0
centi = 0

# mulai main -> putar countdown.mp3 dulu sebelum hitungan jalan
countdown_proc = play_music_tracked(SOUND_COUNTDOWN)
countdown_wait_start = time.time()

try:
    while True:
        if state == "RUNNING":
            elapsed = time.time() - start
            total_centi = int(elapsed * 100) % 10000
            sec = total_centi // 100
            centi = total_centi % 100

            font.clear()
            font.draw_time(sec, centi, RED)
            matrix.SetImage(font.get_image())

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
            # menunggu ENTER berikutnya untuk mulai countdown
            if enter_event.is_set():
                enter_event.clear()
                print("[DEBUG] STOPPED -> mulai COUNTDOWN lagi")
                font.clear()
                font.draw_time(0, 0, YELLOW)
                matrix.SetImage(font.get_image())
                countdown_proc = play_music_tracked(SOUND_COUNTDOWN)
                countdown_wait_start = time.time()
                state = "COUNTDOWN"

        else:  # COUNTDOWN
            # abaikan ENTER yang ditekan selagi musik countdown main
            if enter_event.is_set():
                enter_event.clear()
                print("[DEBUG] ENTER diabaikan (masih COUNTDOWN)")

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
