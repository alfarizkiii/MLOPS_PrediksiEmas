import os
import datetime
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

# 1. Konfigurasi Alamat MLflow Tracking Server
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_URI)

client = MlflowClient()
MODEL_NAME = "Gold_Price_Predictor"

print("\n" + "="*50)
print("=== STARTING AUTOMATED RETRAINING PIPELINE ===")
print("="*50)

# 2. Tarik Data Historis Paling Segar dari yfinance (1 Tahun Terakhir)
today = datetime.date.today()
start_date = today - datetime.timedelta(days=365)
print(f"[*] Menarik data historis emas (GC=F) dari {start_date} hingga {today}...")

try:
    df = yf.download("GC=F", start=start_date, end=today)
    if df.empty:
        raise ValueError("Data yang diunduh kosong.")
except Exception as e:
    print(f"[!] Gagal mengunduh data dari yfinance: {e}")
    exit(1)

# Preprocessing Kilat
df = df.dropna()
X = df[['Open', 'High', 'Low', 'Volume']]
y = df['Close']

# 3. Latih Model Baru
print("[*] Memulai pelatihan model baru dengan data tren terkini...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
# PERBAIKAN WARNING: Meratakan dimensi data target menjadi 1D array
model.fit(X, y.values.ravel())

# 4. Evaluasi Performa Model Baru
predictions = model.predict(X)
# PERBAIKAN ERROR: Menghitung RMSE tanpa bergantung pada parameter 'squared' yang sudah usang
mse = mean_squared_error(y, predictions)
new_rmse = mse ** 0.5
print(f"[+] Pelatihan selesai. RMSE Model Baru: {new_rmse:.4f}")

# 5. Catat dan Registrasikan Model Baru ke MLflow Tracking
with mlflow.start_run() as run:
    run_id = run.info.run_id
    mlflow.log_metric("rmse", new_rmse)
    mlflow.log_param("n_estimators", 100)
    
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )
    print(f"[+] Model sukses dicatat di MLflow Registry (Run ID: {run_id})")

# 6. GERBANG VALIDASI & OTOMASI PROMOSI
print("[*] Menghubungi MLflow Registry untuk proses validasi kelayakan...")
try:
    latest_production = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    
    if latest_production:
        prod_version = latest_production[0]
        prod_run_id = prod_version.run_id
        
        prod_run = client.get_run(prod_run_id)
        prod_rmse = prod_run.data.metrics.get("rmse", float('inf'))
        print(f"[*] Model Production Saat Ini (Versi {prod_version.version}) memiliki RMSE: {prod_rmse:.4f}")
        
        if new_rmse < prod_rmse:
            print("[✓] VALIDASI LULUS: Model baru terbukti lebih akurat!")
            
            latest_none_versions = client.get_latest_versions(MODEL_NAME, stages=["None"])
            new_version = latest_none_versions[0].version
            
            client.transition_model_version_stage(
                name=MODEL_NAME,
                version=new_version,
                stage="Production",
                archive_existing_versions=True
            )
            print(f"[✓] SUKSES: Model Versi {new_version} resmi naik pangkat ke PRODUCTION!")
        else:
            print("[X] VALIDASI GAGAL: Model baru tidak lebih baik dari model Production saat ini.")
            print("[*] Keputusan: Model baru dibiarkan di laci, sistem tetap menggunakan model Production lama.")
    else:
        latest_none_versions = client.get_latest_versions(MODEL_NAME, stages=["None"])
        new_version = latest_none_versions[0].version
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=new_version,
            stage="Production"
        )
        print(f"[✓] Inisialisasi: Laci Production kosong. Model Versi {new_version} langsung diangkat ke PRODUCTION.")

except Exception as e:
    print(f"[!] Terjadi error saat proses auto-promosi: {e}")

print("="*50 + "\n")