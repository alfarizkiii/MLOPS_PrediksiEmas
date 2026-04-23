import os
import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def main():
    # Setup argument parser untuk variasi eksperimen dari terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=10)
    args = parser.parse_args()

    # 1. Load Data (Hasil dari LK-05)
    data_path = "data/processed/gold_cleaned.csv"
    try:
        data = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error loading data: {e}. Pastikan file ada di {data_path}")
        return

    # Asumsi kolom standar Yahoo Finance: Date, Open, High, Low, Close, Adj Close, Volume
    # Kita prediksi 'Close' berdasarkan 'Open', 'High', 'Low', 'Volume'
    features = ['Open', 'High', 'Low', 'Volume']
    
    # Hapus baris yang mungkin memiliki nilai kosong di fitur atau target
    data = data.dropna(subset=features + ['Close'])

    X = data[features]
    y = data['Close']

    # Split data (shuffle=False karena ini data time-series)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Set nama eksperimen di MLflow
    mlflow.set_experiment("Gold_Price_Prediction")

    # 3. Logging Eksperimen MLflow
    with mlflow.start_run():
        print(f"Running experiment with n_estimators={args.n_estimators}, max_depth={args.max_depth}")
        
        # Inisialisasi dan latih model
        rf = RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
        rf.fit(X_train, y_train)

        # Prediksi
        predictions = rf.predict(X_test)

        # Evaluasi
        rmse, mae, r2 = eval_metrics(y_test, predictions)
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        # MLflow Log Parameters
        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_param("model_type", "RandomForestRegressor")

        # MLflow Log Metrics
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # MLflow Log Model
        mlflow.sklearn.log_model(rf, "model")

if __name__ == "__main__":
    main()