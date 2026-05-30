from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import os
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge

app = FastAPI(title="Gold Price Predictor API with Observability")

# 1. Deklarasi Metrik Custom untuk mendeteksi pergerakan prediksi emas
PREDICTION_SCORE = Gauge('gold_prediction_score', 'Predicted closing price of gold')

# 2. Inisialisasi Instrumentator untuk membaca Latensi & Throughput
Instrumentator().instrument(app).expose(app)

# 3. Setup parameter dari Environment Variables
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "Gold_Price_Predictor")
STAGE = os.getenv("MODEL_STAGE", "Production")

mlflow.set_tracking_uri(MLFLOW_URI)

class GoldData(BaseModel):
    Open: float
    High: float
    Low: float
    Volume: float

# Variabel penampung model
model = None

@app.post("/predict")
def predict_gold_price(data: GoldData):
    global model
    
    # LAZY LOADING: Coba muat model jika masih kosong
    if model is None:
        try:
            model_uri = f"models:/{MODEL_NAME}/{STAGE}"
            model = mlflow.pyfunc.load_model(model_uri)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal memuat model dari MLflow: {str(e)}")
            
    try:
        # Format data dan lakukan prediksi
        input_data = [[data.Open, data.High, data.Low, data.Volume]]
        prediction = model.predict(input_data)
        pred_value = float(prediction[0])
        
        # 4. SET METRIK CUSTOM: Kirim angka tebakan ke Prometheus
        PREDICTION_SCORE.set(pred_value)
        
        return {
            "model_version": STAGE,
            "predicted_close_price": round(pred_value, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediksi: {str(e)}")