#!/usr/bin/env python3
"""
generate_pdf_report.py
Menghasilkan dokumen PDF formal laporan teknis integrasi API dan penentuan lokasi
display SenkaLed tanpa format bergaya kecerdasan buatan (tanpa butir peluru/bullet,
tanpa garis pemisah dekoratif, dan disajikan dalam narasi teknis baku).
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        # Header kecil
        self.drawString(54, 800, "Laporan Teknis Sistem Display SenkaLed — Integrasi API & Lokasi Observasi")
        # Footer nomor halaman
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(A4[0] - 54, 40, page_text)
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,   # 1.9 cm margin
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Definisi gaya paragraf formal
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        alignment=TA_LEFT,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        alignment=TA_JUSTIFY,
        firstLineIndent=20,
        spaceAfter=6
    )

    code_block_style = ParagraphStyle(
        'CodeBlockCustom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_LEFT,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # Judul Dokumen
    story.append(Paragraph("LAPORAN TEKNIS INTEGRASI DATA CUACA DAN INDEKS ULTRAVIOLET", title_style))
    story.append(Paragraph("PADA SISTEM DISPLAY LED MATRIX SENKA", title_style))
    story.append(Paragraph("Lokasi Observasi: Koridor Senayan, Jakarta Pusat / Selatan<br/>Dokumentasi Implementasi Perangkat Lunak dan Jaringan", subtitle_style))
    story.append(Spacer(1, 10))

    # Bab 1
    story.append(Paragraph("1. Pendahuluan", heading_style))
    story.append(Paragraph(
        "Laporan teknis ini disusun untuk mendokumentasikan implementasi sistem penarikan data cuaca dan indeks radiasi ultraviolet yang diterapkan pada perangkat display LED panel matrix SenkaLed. Sistem ini dibangun guna menunjang aktivasi stan promosi produk Senka melalui penyajian informasi lingkungan luar ruang yang aktual kepada publik. Pembahasan dalam dokumen ini mencakup landasan penentuan koordinat pemantauan, pemilihan penyedia antarmuka pemrograman aplikasi atau Application Programming Interface (API), format pertukaran data numerik, pemetaan visual pada modul perangkat keras, serta protokol penanganan konektivitas jaringan selama kegiatan berlangsung.",
        body_style
    ))

    # Bab 2
    story.append(Paragraph("2. Spesifikasi Lokasi dan Karakteristik Lingkungan", heading_style))
    story.append(Paragraph(
        "Pemantauan parameter cuaca dan paparan radiasi matahari dikunci secara permanen pada titik koordinat lintang -6.224413119718039 dan bujur 106.80386768026403 dengan elevasi daratan sekitar 19 meter di atas permukaan laut. Posisi geografis ini berkedudukan tepat di koridor Senayan, di antara kawasan Gelora Bung Karno dan FX Sudirman, DKI Jakarta.",
        body_style
    ))
    story.append(Paragraph(
        "Penetapan titik observasi tersebut merujuk langsung pada lokasi penyelenggaraan pameran interaktif Senka yang berada di kawasan dengan konsentrasi aktivitas pejalan kaki yang padat. Secara klimatologis, wilayah metropolitan Jakarta memiliki tingkat radiasi ultraviolet permukaan yang sangat signifikan sepanjang tahun. Pada rentang waktu tengah hari antara pukul 10.30 hingga 14.00 WIB, indeks ultraviolet di titik koordinat ini secara konsisten menyentuh angka 8 hingga 10, yang diklasifikasikan sebagai tingkatan berisiko sangat tinggi bagi kesehatan jaringan kulit. Penyajian data real-time setempat ini berfungsi sebagai sarana komunikasi berbasis data faktual yang secara langsung mengedukasi pengunjung mengenai urgensi penggunaan produk perlindungan tabir surya Senka.",
        body_style
    ))

    # Bab 3
    story.append(Paragraph("3. Penyedia Antarmuka Pemrograman Aplikasi (API)", heading_style))
    story.append(Paragraph(
        "Sistem menggunakan layanan data meteorologi terpadu dari Open-Meteo Weather and Solar Radiation Service. Pemilihan penyedia layanan ini didasarkan pada keandalan infrastruktur dan kesesuaian operasional untuk perangkat tertanam mikrokomputer Raspberry Pi. Open-Meteo menyatukan model peramalan numerik resolusi tinggi dari berbagai institusi meteorologi dunia, meliputi model ICON dari Deutscher Wetterdienst, model IFS dari European Centre for Medium-Range Weather Forecasts, serta Global Forecast System dari National Oceanic and Atmospheric Administration Amerika Serikat.",
        body_style
    ))
    story.append(Paragraph(
        "Keunggulan teknis mendasar dari arsitektur ini adalah ketiadaan kewajiban penggunaan kunci token otentikasi atau API key. Dengan ditiadakannya ketergantungan pada token privat, potensi kegagalan sistem di lapangan akibat habisnya kuota permintaan harian, pembatasan lalu lintas mendadak dari penyedia server, ataupun masa kedaluwarsa akun dapat dieliminasi secara menyeluruh, sehingga display dapat beroperasi tanpa risiko penghentian sepihak.",
        body_style
    ))

    # Bab 4
    story.append(Paragraph("4. Format Permintaan dan Struktur Pertukaran Data", heading_style))
    story.append(Paragraph(
        "Komunikasi antara mikrokomputer lokal dan peladen data berlangsung melalui protokol transmisi aman HTTPS menggunakan metode permintaan GET dengan alamat endpoint terprogram sebagai berikut:",
        body_style
    ))
    story.append(Paragraph(
        "https://api.open-meteo.com/v1/forecast?latitude=-6.224413&amp;longitude=106.803868&amp;current=temperature_2m,uv_index&amp;timezone=Asia%2FJakarta",
        code_block_style
    ))
    story.append(Paragraph(
        "Konfigurasi parameter alamat di atas memuat instruksi koordinat lintang dan bujur lokasi Senayan. Parameter current dispesifikasikan hanya meminta dua variabel utama, yaitu temperature_2m untuk temperatur udara pada elevasi standar dua meter dalam satuan derajat Celcius, serta uv_index untuk besaran indeks radiasi ultraviolet permukaan. Penggunaan parameter zona waktu Asia/Jakarta sangat krusial guna mengikat posisi sudut datang matahari terhadap waktu lokal Indonesia Barat secara tepat, sehingga fluktuasi indeks radiasi sejak fajar hingga senja sejalan dengan kondisi insolasi nyata di Jakarta.",
        body_style
    ))
    story.append(Paragraph(
        "Respon balik yang diterima oleh mikrokomputer berbentuk berkas terstruktur JavaScript Object Notation (JSON) berukuran sangat ringkas sekitar 500 bita. Nilai desimal temperatur dan indeks ultraviolet yang diterima diurai secara langsung, kemudian dibulatkan ke bilangan bulat terdekat untuk kenyamanan visual pemirsa. Angka indeks radiasi kemudian diterjemahkan secara otomatis mengikuti standar klasifikasi World Health Organization (WHO), yaitu kategori rendah untuk indeks di bawah 3, menengah untuk indeks 3 hingga 5, tinggi untuk indeks 6 hingga 7, sangat tinggi untuk indeks 8 hingga 10, dan ekstrem untuk indeks 11 ke atas.",
        body_style
    ))

    # Bab 5
    story.append(Paragraph("5. Pemetaan Visual Perangkat Keras dan Tipografi", heading_style))
    story.append(Paragraph(
        "Data numerik yang telah diolah selanjutnya dirender ke dalam kanvas digital beresolusi 96 x 16 piksel yang dibentuk oleh tiga unit panel P10 LED RGB jenis HUB75 berukuran 32 x 16 piksel yang dirangkai secara seri mendatar. Pembagian bidang layar dibagi secara simetris menjadi tiga kompartemen informasi.",
        body_style
    ))
    story.append(Paragraph(
        "Panel pertama pada sektor kiri didedikasikan untuk menampilkan nilai suhu udara dalam format angka dan simbol satuan. Panel kedua pada sektor tengah memuat teks label UV INDEX pada baris atas serta nilai angka indeks radiasi pada baris bawah. Panel ketiga pada sektor kanan menyajikan klasifikasi tingkat risiko paparan matahari dalam format dua baris teks terpisah. Seluruh karakter digambar menggunakan struktur matriks font monokrom dengan tinggi seragam lima piksel serta margin pembatas di sekeliling bidang agar tidak menyentuh bingkai luar panel. Guna menghasilkan reproduksi warna biru khas Senka yang murni dan menghindari distorsi spektrum optik pada lampu semikonduktor, sinyal pewarnaan dikalibrasikan melalui koreksi urutan kanal BGR pada lapisan perangkat keras driver.",
        body_style
    ))

    # Bab 6
    story.append(Paragraph("6. Manajemen Keandalan Sistem dan Mitigasi Jaringan", heading_style))
    story.append(Paragraph(
        "Guna menjamin keandalan sistem selama pameran berlangsung, arsitektur perangkat lunak memisahkan proses penggambaran visual display dengan proses komunikasi internet ke dalam dua alur kerja terpisah atau multithreading. Alur kerja utama bertugas menyalakan panel LED secara kontinu tanpa jeda, sementara alur kerja latar belakang bertugas memeriksa pembaruan data secara berkala.",
        body_style
    ))
    story.append(Paragraph(
        "Interval penarikan data normal ditetapkan setiap 600 detik atau sepuluh menit sekali. Periode ini merupakan interval optimal karena perubahan temperatur makro dan radiasi matahari tidak berlangsung secara fraksional detik, sekaligus sangat menghemat kuota transmisi seluler di lokasi. Apabila sambungan internet nirkabel di area stan pameran terputus atau mengalami gangguan teknis, sistem tidak akan mengalami kegagalan proses atau layar padam. Program secara otomatis mempertahankan data valid terakhir pada memori aktif serta menyimpan salinannya ke dalam berkas fisik penyimpanan lokal weather_cache.json.",
        body_style
    ))
    story.append(Paragraph(
        "Dalam status luring tersebut, sistem mengalihkan siklus pemeriksaan ke mode percobaan ulang cepat setiap 30 detik. Segera setelah sambungan internet tersambung kembali, sistem akan melakukan sinkronisasi data seketika dan mengembalikan interval pembaruan ke siklus normal tanpa memerlukan pengaturan ulang manual dari teknisi operasional.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF berhasil dibuat: {filename}")


if __name__ == "__main__":
    out_dir = r"c:\Users\USER\CODX\SenkaLed"
    target_pdf = os.path.join(out_dir, "Laporan_Teknis_Integrasi_API_SenkaLed.pdf")
    build_pdf(target_pdf)
    
    # Salin juga ke artifact dir
    artifact_dir = r"C:\Users\USER\.gemini\antigravity\brain\df4c96da-b715-4972-82fd-243c5bf03747"
    if os.path.exists(artifact_dir):
        artifact_pdf = os.path.join(artifact_dir, "Laporan_Teknis_Integrasi_API_SenkaLed.pdf")
        import shutil
        shutil.copy2(target_pdf, artifact_pdf)
        print(f"Salinan disimpan ke artifact: {artifact_pdf}")
