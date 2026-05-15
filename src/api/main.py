from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import os

app = FastAPI(title="Gold Price Predictor API")

# Setup parameter dari Environment Variables (diisi oleh Docker Compose nanti)
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "Gold_Price_Predictor")
STAGE = os.getenv("MODEL_STAGE", "Production")

mlflow.set_tracking_uri(MLFLOW_URI)

class GoldData(BaseModel):
    Open: float
    High: float
    Low: float
    Volume: float

@app.post("/predict")
def predict_gold_price(data: GoldData):
    try:
        # Menarik model dinamis dari MLflow
        model_uri = f"models:/{MODEL_NAME}/{STAGE}"
        model = mlflow.pyfunc.load_model(model_uri)
        
        # Format data dan lakukan prediksi
        input_data = [[data.Open, data.High, data.Low, data.Volume]]
        prediction = model.predict(input_data)
        
        return {
            "model_version": STAGE,
            "predicted_close_price": round(float(prediction[0]), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prediksi: {str(e)}")