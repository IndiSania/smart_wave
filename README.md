# SmartWaste AI ♻️

SmartWaste AI adalah aplikasi computer vision berbasis Python untuk membantu mendeteksi objek pada gambar dan memetakan objek tersebut ke kategori pengelolaan sampah.

## Fitur

- Deteksi objek menggunakan YOLO dari Ultralytics
- Input gambar dari upload atau kamera
- Pengaturan ambang kepercayaan deteksi
- Kategori Organik, Anorganik, Kertas, Elektronik, dan Lainnya
- Rekomendasi pengelolaan untuk setiap objek
- Visualisasi bounding box
- Riwayat analisis lokal
- Dashboard Streamlit dengan tampilan profesional
- Struktur kode modular agar mudah dikembangkan

## Teknologi

- Python
- Streamlit
- Ultralytics YOLO
- OpenCV
- Pillow
- NumPy

## Cara menjalankan

### 1. Pastikan Python tersedia

Disarankan Python 3.11 atau 3.12 untuk kompatibilitas library computer vision.

### 2. Buat virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install library

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```bash
streamlit run app.py
```

Browser akan membuka aplikasi SmartWaste AI.

## Model

Aplikasi menggunakan model YOLO kecil dari Ultralytics. Jika file model belum tersedia di folder `models`, Ultralytics dapat mengunduh model pada penggunaan pertama.

Untuk versi produksi, model umum dapat diganti dengan model yang dilatih khusus menggunakan dataset sampah.

## Alur sistem

Input gambar
→ YOLO mendeteksi objek
→ sistem membaca label dan confidence
→ label dipetakan ke kategori sampah
→ rekomendasi pengelolaan ditampilkan
→ hasil dapat disimpan ke riwayat

## Struktur proyek

```text
SmartWaste_Professional/
├── app.py
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── detector.py
│   ├── ui.py
│   └── utils.py
├── assets/
├── data/
│   └── history.json
├── models/
└── tests/
```

## Pengembangan lanjutan

1. Melatih model khusus dataset sampah.
2. Menambah login admin.
3. Menambah database MySQL/PostgreSQL.
4. Menambah statistik berdasarkan kategori.
5. Menambah ekspor laporan CSV/PDF.
6. Menambahkan halaman edukasi pemilahan sampah.
7. Menambahkan API untuk integrasi aplikasi lain.

## Catatan akurasi

Hasil deteksi sangat bergantung pada model, pencahayaan, sudut kamera, kualitas gambar, dan objek yang terlihat. Kategori pada versi ini adalah pemetaan berbasis label objek, bukan penentuan material secara kimiawi.
