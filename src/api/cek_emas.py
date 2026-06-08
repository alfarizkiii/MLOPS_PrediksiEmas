import yfinance as yf
import requests

print("=== DATA EMAS TERBARU ===")
gold = yf.Ticker("GC=F")
hari_ini = gold.history(period="1d")

if not hari_ini.empty:
    # 1. Mengambil data dari Yahoo Finance
    open_price = float(hari_ini['Open'].iloc[0])
    high_price = float(hari_ini['High'].iloc[0])
    low_price = float(hari_ini['Low'].iloc[0])
    volume = float(hari_ini['Volume'].iloc[0])
    close_asli = float(hari_ini['Close'].iloc[0])
    
    print(f"Tanggal : {hari_ini.index[0].strftime('%Y-%m-%d')}")
    print(f"Open    : {open_price:.2f}")
    print(f"High    : {high_price:.2f}")
    print(f"Low     : {low_price:.2f}")
    print(f"Volume  : {int(volume)}")
    print(f"Close   : {close_asli:.2f}")
    
    # 2. Mengotomatisasi pemanggilan API (Pengganti cURL manual)
    print("\n=== MENGIRIM DATA KE API UNTUK DIPREDIKSI ===")
    url = "http://localhost:8000/predict"
    payload = {
        "Open": open_price,
        "High": high_price,
        "Low": low_price,
        "Volume": volume
    }
    
    try:
        # Menembak API secara otomatis
        response = requests.post(url, json=payload)
        hasil = response.json()
        
        tebakan_model = hasil.get('predicted_close_price')
        versi_model = hasil.get('model_version')
        
        print(f"Versi Model Aktif : {versi_model}")
        print(f"Tebakan API Model : {tebakan_model}")
        print(f"Harga Penutupan Asli: {close_asli:.2f}")
        
        # Menghitung seberapa meleset modelmu hari ini
        selisih = abs(tebakan_model - close_asli)
        print(f"Selisih Error     : {selisih:.2f}")
        
    except requests.exceptions.ConnectionError:
        print("[!] Gagal terhubung. Pastikan container API (port 8000) sedang menyala!")
else:
    print("Data hari ini belum tersedia.")