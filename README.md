**Nama:** Muhammad Naufal Al Farizki

**NIM:** 235150207111032

**Program Studi:** Teknik Informatika (Angkatan 2023)

**Institusi:** Fakultas Ilmu Komputer (FILKOM), Universitas Brawijaya

# MLOPS_PrediksiEmas : Sistem Prediksi Harga Emas Adaptif

Repositori ini berisi fondasi teknis untuk inisiasi proyek pengembangan Sistem Prediksi Harga Emas (XAU/USD) berbasis Machine Learning Operations (MLOps). 

## Tujuan Proyek
Proyek ini bertujuan untuk membangun sistem prediksi harga emas *time-series* secara *real-time* menggunakan data dari API `yfinance`. Sistem ini dirancang berorientasi *production* dengan menerapkan strategi *Continual Learning* (CT) untuk mendeteksi dan menangani *Data Drift* (perubahan tren dan volatilitas pasar) agar model tetap relevan.

## 📂 Struktur Direktori
Proyek ini mengadopsi standar konvensi industri **Cookiecutter Data Science** yang diperluas dengan arsitektur MLOps untuk memastikan kerapian dan reproduktibilitas:

* `.github/workflows/` : Pipa CI/CD (`automation.yml`) dan *Continuous Training* (`ct_pipeline.yml`).
* `config/` : Berisi fail konfigurasi *environment*, parameter, dan kredensial (diabaikan git).
* `data/` : Penyimpanan data dari `yfinance` (`raw/`, `interim/`, `processed/`, `external/`).
* `docker/` : Konfigurasi *container* (`api.Dockerfile`, `mlflow.Dockerfile`).
* `models/` : Tempat menyimpan artefak model ML (*tracking* via MLflow).
* `notebooks/` : Jupyter notebooks untuk eksplorasi data (EDA).
* `reports/` : Laporan hasil evaluasi dan visualisasi (`figures/`).
* `scripts/` : Skrip otomatisasi tingkat lanjut (termasuk `retrain.py` untuk CT).
* `src/` : *Source code* utama (ETL data, *features*, dan `api/` untuk mikroservis).
* `docker-compose.yaml` : Orkestrasi kluster infrastruktur (6 layanan terintegrasi).
* `prometheus.yml` : Konfigurasi *scraping* metrik pemantauan.

## 💻 Persiapan Lingkungan (GitHub Codespaces)
Agar proyek bersifat *reproducible* dan bebas dari masalah dependensi, proyek ini menggunakan lingkungan virtual GitHub Codespaces yang dikonfigurasi melalui `.devcontainer`.

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

### 4. Pelacakan Versi Data (DVC Tracking)
Sesuai dengan prinsip MLOps, proyek ini memisahkan antara pelacakan kode (Git) dan pelacakan data fisik (DVC) agar repositori tetap ringan. Setiap kali terdapat data baru dari langkah 2, perbarui "sidik jari" data menggunakan DVC:

```bash
dvc add data/raw
dvc diff
```
Ekspektasi Output: DVC akan mencatat modifikasi dan memperbarui berkas metadata data/raw.dvc. Perintah dvc diff akan memvalidasi data drift atau silsilah penambahan file baru secara presisi tanpa memuat CSV ke dalam memori Git.

### 5. Penyimpanan Eksternal (MinIO Remote Storage)
Fisik data CSV dikelola secara independen di luar repositori menggunakan MinIO Object Storage (S3-compatible) yang berjalan di atas container Docker lokal. Untuk menyinkronkan dan mengamankan dataset mentah terbaru ke awan, jalankan:

```bash
dvc push
```

## 🐳 Infrastruktur Layanan Produksi (Docker Compose)

Seluruh arsitektur inferensi dan observabilitas dibungkus menggunakan Docker pada jaringan internal terisolasi. Jalankan perintah ini untuk membangun dan menyalakan 6 kontainer sekaligus (PostgreSQL, MLflow, FastAPI, Prometheus, cAdvisor, Grafana):

```bash
docker-compose up -d --build

```

Setelah seluruh kontainer berstatus `Running`, akses layanan melalui *browser*:

* **FastAPI Swagger UI:** `http://localhost:8000/docs`
* **MLflow Tracking Server:** `http://localhost:5000`
* **Grafana Dashboard:** `http://localhost:3000` *(Login default: `admin` / `admin`)*

---

## 🎯 Penggunaan API Prediksi (Inferensi)

Mikroservis FastAPI dilengkapi mekanisme *Lazy Loading* untuk menghemat memori. API menerima *request* berupa data fitur emas (Open, High, Low, Volume) untuk menebak Harga Penutupan (Close).

**Opsi 1: Menggunakan cURL Manual**

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{"Open": 2320.50, "High": 2345.00, "Low": 2310.20, "Volume": 150000}'

```

**Opsi 2: Simulator Live Data Otomatis (Disarankan)**
Skrip ini terhubung langsung ke Yahoo Finance, mengekstrak harga hari ini, mengirimkannya ke API produksi, dan menghitung nilai selisih (*error*) secara *real-time*:

```bash
python src/api/cek_emas.py

```

---

## 📊 Observabilitas & Pemantauan (Monitoring)

Sistem memantau metrik perangkat keras (CPU/RAM via cAdvisor) dan perangkat lunak secara *real-time*. Pada Grafana Alerting, ditetapkan ambang batas (*threshold*) keamanan untuk metrik khusus `gold_prediction_score`:

* **Batas Atas (Bubble):** $3500.00
* **Batas Bawah (Crash):** $1200.00

Jika prediksi melampaui batas tersebut selama lebih dari 1 menit akibat lonjakan pasar, sistem otomatis berubah status menjadi `Firing` dan memicu mekanisme perlindungan CT via *Webhook*.

---

## 🔄 Continuous Training (CT) & Evaluasi Komparatif

Model dilatih ulang dan divalidasi secara otomatis tanpa intervensi manusia menggunakan **GitHub Actions** (`ct_pipeline.yml`) yang dipicu oleh:

1. **Jadwal Rutin (Cron):** Berjalan otomatis setiap hari Minggu pukul 00:00 UTC.
2. **Alarm Darurat:** Dipicu seketika oleh *Repository Dispatch Webhook* dari Grafana.

**Gerbang Validasi MLflow (Closed-Loop):**
Ketika skrip `scripts/retrain.py` berjalan, model baru akan dibandingkan secara matematis dengan model *Production* lama. Model baru hanya akan dipromosikan (menggantikan model lama tanpa *downtime*) **JIKA DAN HANYA JIKA** terbukti memiliki nilai *Root Mean Squared Error* (RMSE) yang lebih kecil/lebih akurat. Jika tidak, model baru akan diisolasi.

---
