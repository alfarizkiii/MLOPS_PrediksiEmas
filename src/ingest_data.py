import yfinance as yf
import os
from datetime import datetime

# Mengatur path secara otomatis agar dinamis
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Jika script ini ditaruh langsung di folder src/, gunakan ini:
RAW_DIR = os.path.join(BASE_DIR, "data", "raw") 

def ingest_data():
    print("Memulai Data Ingestion dari Yahoo Finance...")
    
    # Menarik data emas (1 bulan terakhir)
    data = yf.download("GC=F", period="1mo", interval="1d")
    
    # Memastikan folder data/raw/ tersedia
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # Membuat format timestamp: TahunBulanHari_JamMenitDetik
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(RAW_DIR, f"gold_raw_{timestamp}.csv")
    
    # Menyimpan data mentah
    data.to_csv(file_path)
    print(f"Sukses! Data mentah berhasil disimpan di:\n{file_path}")

if __name__ == "__main__":
    ingest_data()