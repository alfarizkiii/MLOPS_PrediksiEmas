import mlflow.pyfunc
import pandas as pd

def main():
    # Memanggil model secara dinamis berdasarkan status 'Production'
    model_name = "Gold_Price_Predictor"
    stage = "Production"

    print(f"Loading model '{model_name}' dari stage '{stage}'...")

    # Format URI resmi MLflow untuk mengambil model production
    model_uri = f"models:/{model_name}/{stage}"

    try:
        # Load model
        model = mlflow.pyfunc.load_model(model_uri)
        print("Model berhasil dimuat!\n")

        # Membuat data dummy untuk simulasi prediksi (Open, High, Low, Volume)
        dummy_data = pd.DataFrame([{
            'Open': 2300.50,
            'High': 2315.00,
            'Low': 2295.20,
            'Volume': 150000
        }])

        print("Mencoba melakukan inferensi prediksi harga penutupan (Close)...")
        prediction = model.predict(dummy_data)
        print(f"Hasil Prediksi Harga Close: ${prediction[0]:.2f}")

    except Exception as e:
        print(f"Gagal memuat model atau inferensi: {e}")

if __name__ == "__main__":
    main()