import yfinance as yf

# Mengambil data emas berjangka (Gold Futures)
gold = yf.Ticker("GC=F")

# Menarik data 1 hari terakhir
hari_ini = gold.history(period="1d")

if not hari_ini.empty:
    print("=== DATA EMAS TERBARU ===")
    print(f"Tanggal : {hari_ini.index[0].strftime('%Y-%m-%d')}")
    print(f"Open    : {hari_ini['Open'].iloc[0]:.2f}")
    print(f"High    : {hari_ini['High'].iloc[0]:.2f}")
    print(f"Low     : {hari_ini['Low'].iloc[0]:.2f}")
    print(f"Volume  : {int(hari_ini['Volume'].iloc[0])}")
    print(f"Close   : {hari_ini['Close'].iloc[0]:.2f}")
else:
    print("Data hari ini belum tersedia.")