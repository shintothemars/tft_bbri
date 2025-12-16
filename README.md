# 📈 BBRI Stock Prediction System

Aplikasi web untuk prediksi harga saham Bank Rakyat Indonesia (BBRI) menggunakan **Temporal Fusion Transformer (TFT)** model dengan Django REST Framework backend dan React frontend.

## 🎯 Fitur Utama

- ✅ Prediksi harga saham BBRI hingga 30 hari ke depan
- ✅ Visualisasi interaktif dengan Bokeh (confidence intervals)
- ✅ Data real-time dari Yahoo Finance
- ✅ Analisis tren dalam bahasa yang mudah dipahami
- ✅ UI modern dan responsif
- ✅ Indikator teknikal otomatis (MA, RSI, MACD, Bollinger Bands)

## 🏗️ Struktur Proyek

```
tft_bbri/
├── backend/                    # Django REST Framework
│   ├── bbri_backend/          # Project settings
│   ├── predictor/             # Prediction app
│   │   ├── model.py           # TFT model loader
│   │   ├── views.py           # API endpoints
│   │   └── urls.py            # URL routing
│   ├── manage.py
│   └── requirements.txt
├── frontend/                   # React Application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx           # Main app
│   │   └── index.css         # Styling
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── best_tft_model.pth         # Trained TFT model
└── README.md
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm atau yarn

## 🚀 Instalasi

### Backend (Django)

1. **Buat virtual environment:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

3. **Jalankan migrasi database:**
```powershell
python manage.py migrate
```

4. **Jalankan development server:**
```powershell
python manage.py runserver
```

Backend akan berjalan di `http://localhost:8000`

### Frontend (React)

1. **Install dependencies:**
```powershell
cd frontend
npm install
```

2. **Jalankan development server:**
```powershell
npm run dev
```

Frontend akan berjalan di `http://localhost:3000`

## 🎮 Cara Menggunakan

1. Buka browser dan akses `http://localhost:3000`
2. Pilih tanggal target prediksi (hari, bulan, tahun)
3. Klik tombol "🔮 Prediksi Sekarang"
4. Tunggu beberapa detik untuk proses prediksi
5. Lihat hasil prediksi dengan visualisasi interaktif

## 📊 API Endpoints

### Health Check
```
GET /api/health/
```

Response:
```json
{
  "status": "healthy",
  "service": "BBRI Stock Prediction API",
  "version": "1.0.0"
}
```

### Predict Stock Price
```
POST /api/predict/
Content-Type: application/json

{
  "target_date": "2025-12-31"
}
```

Response:
```json
{
  "success": true,
  "target_date": "2025-12-31",
  "last_data_date": "2025-12-16",
  "prediction_horizon": 15,
  "predictions": {
    "dates": ["2025-12-17", "2025-12-18", ...],
    "median": [5200, 5250, ...],
    "lower_bound": [5100, 5150, ...],
    "upper_bound": [5300, 5350, ...]
  },
  "historical": {
    "dates": [...],
    "close": [...]
  },
  "analysis": {
    "last_price": 5150,
    "predicted_price": 5280,
    "trend_percentage": 2.52,
    "trend_direction": "NAIK",
    "confidence_range": {
      "lower": 5180,
      "upper": 5380
    }
  },
  "bokeh_plot": {...}
}
```

## 🔧 Teknologi yang Digunakan

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API framework
- **PyTorch** - Deep learning framework
- **pytorch-forecasting** - Time series forecasting
- **yfinance** - Stock data fetching
- **Bokeh** - Interactive visualization
- **ta** - Technical analysis indicators

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **date-fns** - Date utilities
- **Bokeh.js** - Chart rendering

## 📈 Model Information

Model yang digunakan adalah **Temporal Fusion Transformer (TFT)** dengan spesifikasi:
- **Max Encoder Length:** 60 hari
- **Max Prediction Length:** 30 hari
- **Hidden Size:** 32
- **Attention Heads:** 2
- **Output Quantiles:** 7 (0.02, 0.1, 0.25, 0.5, 0.75, 0.9, 0.98)

### Features yang Digunakan:
- **Price Data:** Open, High, Low, Close, Volume
- **Technical Indicators:** MA7, MA30, RSI, MACD, MACD Signal, Bollinger Bands

## ⚠️ Disclaimer

Prediksi ini dibuat menggunakan model machine learning dan **BUKAN merupakan saran investasi**. 
Harga saham dipengaruhi oleh banyak faktor yang tidak dapat sepenuhnya diprediksi. 
Selalu lakukan riset mendalam dan konsultasi dengan ahli keuangan sebelum membuat keputusan investasi.

## 🐛 Troubleshooting

### Backend Issues

**Error: Model file not found**
- Pastikan file `best_tft_model.pth` ada di root directory project
- Check path di `backend/bbri_backend/settings.py`

**Error: yfinance connection**
- Check koneksi internet
- Yahoo Finance mungkin sedang down, coba lagi nanti

### Frontend Issues

**Error: Cannot connect to backend**
- Pastikan backend Django sudah running di port 8000
- Check proxy settings di `vite.config.js`

**Bokeh plot not showing**
- Pastikan Bokeh CDN loaded (check browser console)
- Clear browser cache dan reload

## 📝 Development Notes

### Menambah Fitur Baru

1. **Backend:** Tambahkan endpoint baru di `predictor/views.py`
2. **Frontend:** Buat component baru di `src/components/`
3. **Styling:** Update `src/index.css`

### Testing

Backend:
```powershell
cd backend
python manage.py test
```

Frontend:
```powershell
cd frontend
npm run test
```

## 📧 Contact

Untuk pertanyaan atau issues, silakan buka issue di repository ini.

## 📄 License

This project is for educational purposes.

---

**Developed with ❤️ using Django & React**
