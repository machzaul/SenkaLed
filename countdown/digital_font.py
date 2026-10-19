from PIL import Image
# ==================================================
# MICRO 7 SEGMENT FONT
# PANEL P10 32x16
# 2 MODE:
#   - draw_time()       -> format SS:MS   (font besar, 4 digit)
#   - draw_time_micro() -> format SS:CS:MC (font kecil, 6 digit)
# ==================================================
SEGMENTS = {
    "0":"ABCDEF",
    "1":"BC",
    "2":"ABGED",
    "3":"ABGCD",
    "4":"FGBC",
    "5":"AFGCD",
    "6":"AFGECD",
    "7":"ABC",
    "8":"ABCDEFG",
    "9":"AFGBCD",
}

# ---- font besar (dipakai mode 2-grup: SS:MS) ----
BIG_DIGIT_WIDTH  = 6
BIG_DIGIT_HEIGHT = 14
BIG_DIGIT_GAP    = 1
BIG_GROUP_GAP    = 1
BIG_COLON_WIDTH  = 2

# ---- font kecil (dipakai mode 3-grup: SS:CS:MC) ----
SMALL_DIGIT_WIDTH  = 3
SMALL_DIGIT_HEIGHT = 13
SMALL_DIGIT_GAP    = 1
SMALL_GROUP_GAP    = 1
SMALL_COLON_WIDTH  = 1


class DigitalFont:
    def __init__(self,width=32,height=16):
        self.width = width
        self.height = height
        self.image = Image.new(
            "RGB",
            (width,height),
            (0,0,0)
        )
        self.pixel = self.image.load()

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.pixel[x,y]=(0,0,0)

    def draw_box(self,x,y,w,h,color):
        for yy in range(y,y+h):
            for xx in range(x,x+w):
                if (
                    0 <= xx < self.width
                    and
                    0 <= yy < self.height
                ):
                    self.pixel[xx,yy]=color

    # ==================================================
    # FONT BESAR (6px lebar x 14px tinggi)
    # ==================================================
    def draw_digit_big(self,x,y,digit,color):
        seg = SEGMENTS[str(digit)]
        if "A" in seg:
            self.draw_box(x+1, y+0, 4, 2, color)
        if "B" in seg:
            self.draw_box(x+4, y+1, 2, 5, color)
        if "C" in seg:
            self.draw_box(x+4, y+7, 2, 5, color)
        if "D" in seg:
            self.draw_box(x+1, y+12, 4, 2, color)
        if "E" in seg:
            self.draw_box(x, y+7, 2, 5, color)
        if "F" in seg:
            self.draw_box(x, y+1, 2, 5, color)
        if "G" in seg:
            self.draw_box(x+1, y+6, 4, 2, color)

    def draw_colon_big(self,x,y,color):
        self.draw_box(x, y+3, 2, 2, color)
        self.draw_box(x, y+9, 2, 2, color)

    def draw_time(self,sec,centi,color,blink=False):
        """
        Mode 2-grup: gambar waktu format SS:MS di tengah panel (font besar).
        blink=True -> titik dua berkedip mengikuti nilai centi
        (nyala di paruh pertama, mati di paruh kedua tiap detik).
        """
        txt = f"{sec:02d}{centi:02d}"

        total_width = (
            (BIG_DIGIT_WIDTH*4)
            + (BIG_DIGIT_GAP*2)
            + BIG_COLON_WIDTH
            + (BIG_GROUP_GAP*2)
        )
        start_x = (self.width - total_width)//2
        y = (self.height - BIG_DIGIT_HEIGHT)//2

        x = start_x
        show_colon = (not blink) or (centi < 50)

        self.draw_digit_big(x, y, txt[0], color)
        x += BIG_DIGIT_WIDTH + BIG_DIGIT_GAP
        self.draw_digit_big(x, y, txt[1], color)
        x += BIG_DIGIT_WIDTH + BIG_GROUP_GAP

        if show_colon:
            self.draw_colon_big(x, y, color)
        x += BIG_COLON_WIDTH + BIG_GROUP_GAP

        self.draw_digit_big(x, y, txt[2], color)
        x += BIG_DIGIT_WIDTH + BIG_DIGIT_GAP
        self.draw_digit_big(x, y, txt[3], color)

    # ==================================================
    # FONT KECIL (3px lebar x 13px tinggi)
    # ==================================================
    def draw_digit_small(self,x,y,digit,color):
        seg = SEGMENTS[str(digit)]
        if "A" in seg:
            self.draw_box(x, y+0, 3, 1, color)
        if "B" in seg:
            self.draw_box(x+2, y+1, 1, 5, color)
        if "C" in seg:
            self.draw_box(x+2, y+7, 1, 5, color)
        if "D" in seg:
            self.draw_box(x, y+12, 3, 1, color)
        if "E" in seg:
            self.draw_box(x, y+7, 1, 5, color)
        if "F" in seg:
            self.draw_box(x, y+1, 1, 5, color)
        if "G" in seg:
            self.draw_box(x, y+6, 3, 1, color)

    def draw_colon_small(self,x,y,color):
        self.draw_box(x, y+3, 1, 1, color)
        self.draw_box(x, y+9, 1, 1, color)

    def draw_time_micro(self,sec,centi,micro,color,blink=False):
        """
        Mode 3-grup: gambar waktu format SS:CS:MC di tengah panel (font kecil).
        sec   = detik    (00-99)
        centi = centidetik, 1/100 detik (00-99)
        micro = sub-digit lebih presisi, satuan 100 mikrodetik (00-99)
        """
        t_sec   = f"{sec:02d}"
        t_centi = f"{centi:02d}"
        t_micro = f"{micro:02d}"

        total_width = (
            (SMALL_DIGIT_WIDTH*6)
            + (SMALL_DIGIT_GAP*3)
            + (SMALL_COLON_WIDTH*2)
            + (SMALL_GROUP_GAP*4)
        )
        start_x = (self.width - total_width)//2
        y = (self.height - SMALL_DIGIT_HEIGHT)//2

        x = start_x
        show_colon = (not blink) or (centi < 50)

        self.draw_digit_small(x, y, t_sec[0], color)
        x += SMALL_DIGIT_WIDTH + SMALL_DIGIT_GAP
        self.draw_digit_small(x, y, t_sec[1], color)
        x += SMALL_DIGIT_WIDTH + SMALL_GROUP_GAP

        if show_colon:
            self.draw_colon_small(x, y, color)
        x += SMALL_COLON_WIDTH + SMALL_GROUP_GAP

        self.draw_digit_small(x, y, t_centi[0], color)
        x += SMALL_DIGIT_WIDTH + SMALL_DIGIT_GAP
        self.draw_digit_small(x, y, t_centi[1], color)
        x += SMALL_DIGIT_WIDTH + SMALL_GROUP_GAP

        if show_colon:
            self.draw_colon_small(x, y, color)
        x += SMALL_COLON_WIDTH + SMALL_GROUP_GAP

        self.draw_digit_small(x, y, t_micro[0], color)
        x += SMALL_DIGIT_WIDTH + SMALL_DIGIT_GAP
        self.draw_digit_small(x, y, t_micro[1], color)

    def get_image(self):
        # kembalikan copy supaya frame sebelumnya
        # tidak ikut berubah jika self.image dimodifikasi lagi
        return self.image.copy()

    def get_preview(self, scale=10):
        """
        Untuk debugging di PC: perbesar canvas kecil (32x16)
        agar mudah dilihat. NEAREST supaya pixel tetap kotak
        tegas, tidak blur, meniru tampilan panel LED asli.
        """
        return self.image.resize(
            (self.width*scale, self.height*scale),
            Image.NEAREST
        )
