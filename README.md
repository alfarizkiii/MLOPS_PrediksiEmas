# MLOPS_PrediksiEmad : Sistem Prediksi Harga Emas Adaptif

Repositori ini berisi fondasi teknis untuk inisiasi proyek pengembangan Sistem Prediksi Harga Emas (XAU/USD) berbasis Machine Learning Operations (MLOps). 

## Tujuan Proyek
Proyek ini bertujuan untuk membangun sistem prediksi harga emas *time-series* secara *real-time* menggunakan data dari API `yfinance`. Sistem ini dirancang berorientasi *production* dengan menerapkan strategi *Continual Learning* (CT) untuk mendeteksi dan menangani *Data Drift* (perubahan tren dan volatilitas pasar) agar model tetap relevan.

## Struktur Direktori
Proyek ini mengadopsi standar konvensi industri **Cookiecutter Data Science** untuk memastikan kerapian dan reproduktibilitas:

* `config/` : Berisi file konfigurasi *environment*, parameter, dan kredensial.
* `data/` : Penyimpanan data dari `yfinance` (`raw/`, `interim/`, `processed/`, `external/`).
* `models/` : Tempat menyimpan artefak model ML yang telah dilatih.
* `notebooks/` : Jupyter notebooks untuk eksplorasi data (EDA) dan eksperimen awal.
* `reports/` : Menyimpan laporan hasil evaluasi dan visualisasi (`figures/`).
* `src/` : *Source code* utama (terbagi menjadi modul `data/`, `features/`, `models/`, dan `visualization/`).
* `requirements.txt` : Daftar dependensi Python yang dibutuhkan proyek ini.

## Cara Menjalankan Lingkungan (GitHub Codespaces)
Agar proyek bersifat *reproducible* dan bebas dari masalah dependensi (tanpa galat), proyek ini menggunakan lingkungan virtual GitHub Codespaces yang sudah dikonfigurasi melalui `.devcontainer`.
# MLOps - GoldGuard: Sistem Prediksi Harga Emas Adaptif

Repositori ini berisi fondasi teknis untuk inisiasi proyek pengembangan Sistem Prediksi Harga Emas (XAU/USD) berbasis Machine Learning Operations (MLOps). 

## Tujuan Proyek
Proyek ini bertujuan untuk membangun sistem prediksi harga emas *time-series* secara *real-time* menggunakan data dari API `yfinance`. Sistem ini dirancang berorientasi *production* dengan menerapkan strategi *Continual Learning* (CT) untuk mendeteksi dan menangani *Data Drift* (perubahan tren dan volatilitas pasar) agar model tetap relevan.

## Struktur Direktori
Proyek ini mengadopsi standar konvensi industri **Cookiecutter Data Science** untuk memastikan kerapian dan reproduktibilitas:

* `config/` : Berisi file konfigurasi *environment*, parameter, dan kredensial (diabaikan git).
* `data/` : Penyimpanan data dari `yfinance` (`raw/`, `interim/`, `processed/`, `external/`).
* `models/` : Tempat menyimpan artefak model ML yang telah dilatih.
* `notebooks/` : Jupyter notebooks untuk eksplorasi data (EDA) dan eksperimen awal.
* `reports/` : Menyimpan laporan hasil evaluasi dan visualisasi (`figures/`).
* `src/` : *Source code* utama (terbagi menjadi modul `data/`, `features/`, `models/`, dan `visualization/`).
* `requirements.txt` : Daftar dependensi Python yang dibutuhkan proyek ini.

## Cara Menjalankan Lingkungan (GitHub Codespaces)
Agar proyek bersifat *reproducible* dan bebas dari masalah dependensi (tanpa galat), proyek ini menggunakan lingkungan virtual GitHub Codespaces yang sudah dikonfigurasi melalui `.devcontainer`.

Langkah-langkah menjalankan sistem:
1. Buka halaman utama repositori ini di GitHub.
2. Klik tombol hijau **`<> Code`** di pojok kanan atas.
3. Pilih tab **`Codespaces`**.
4. Klik tombol **`Create codespace on main`** (atau klik *codespace* yang sudah aktif).
5. Lingkungan pengembangan (VS Code web) akan terbuka secara otomatis dengan Python dan konfigurasi ekstensi yang sudah terstandarisasi.

## 🚀 Panduan Eksekusi Pipeline Data (ETL)

Proyek ini telah dilengkapi dengan skrip otomatis untuk melakukan penarikan data dinamis (*Data Ingestion*) dan pembersihan data (*Preprocessing*) dari Yahoo Finance API (Ticker: `GC=F`). 

Untuk menyimulasikan aliran data dan menjalankan *pipeline* ini di lingkungan lokal atau GitHub Codespaces, ikuti langkah-langkah berikut:

### 1. Persiapan Lingkungan (Prerequisites)
Pastikan Anda berada di *root directory* repositori ini dan seluruh dependensi telah terinstal. Jika belum, jalankan perintah berikut di terminal:
```bash
pip install -r requirements.txt
# atau secara manual: pip install yfinance pandas
```

### 2. Eksekusi Data Ingestion (Ekstraksi)
Skrip ini akan menarik riwayat harga emas terbaru dan menyimpannya secara historis tanpa menimpa data sebelumnya.
Jalankan perintah berikut di terminal:

```bash
python src/ingest_data.py
```
Ekspektasi Output: Sebuah file CSV baru yang dilengkapi dengan penanda waktu (timestamp) akan otomatis terbuat di dalam direktori data/raw/ (contoh: gold_raw_20260404_221530.csv).

### 3. Eksekusi Data Preprocessing (Pembersihan)
Skrip ini akan memindai folder data/raw/, mengambil file data mentah yang paling mutakhir, dan melakukan pembersihan (imputasi missing values akibat hari libur bursa menggunakan metode Forward Fill).
Jalankan perintah berikut di terminal:

```bash
python src/preprocess.py
``` 
Ekspektasi Output: Sebuah file CSV bersih bernama gold_cleaned.csv akan disimpan di dalam direktori data/processed/. File inilah yang berfungsi sebagai Feature Store dan siap direkayasa fiturnya untuk pelatihan model Machine Learning.