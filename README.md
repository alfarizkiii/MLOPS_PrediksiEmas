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