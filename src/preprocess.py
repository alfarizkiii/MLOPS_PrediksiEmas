import pandas as pd
import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def preprocess_data():
    print("Memulai proses Pembersihan Data...")
    files = glob.glob(os.path.join(RAW_DIR, "gold_raw_*.csv"))
    if not files:
        print("Error: Tidak ada data mentah. Jalankan ingest_data.py dulu.")
        return

    latest_file = max(files, key=os.path.getctime)
    df = pd.read_csv(latest_file, skiprows=2)
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

    print("Membersihkan missing values dengan Forward Fill...")
    df_cleaned = df.ffill().dropna()

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    output_path = os.path.join(PROCESSED_DIR, "gold_cleaned.csv")
    df_cleaned.to_csv(output_path, index=False)
    print(f"Sukses! Data bersih disimpan di: {output_path}")

if __name__ == "__main__":
    preprocess_data()