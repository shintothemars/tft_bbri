# 📊 Sample Data Mode - Panduan

## Apa itu Sample Data Mode?

Ketika Yahoo Finance tidak dapat diakses (karena koneksi internet, firewall, atau pembatasan API), aplikasi akan otomatis beralih ke **Sample Data Mode** untuk tetap dapat mendemonstrasikan fungsionalitas prediksi.

## Kapan Sample Data Digunakan?

Sample data akan digunakan secara otomatis ketika:
- ❌ Tidak ada koneksi internet
- ❌ Yahoo Finance sedang down atau maintenance
- ❌ Firewall memblokir akses ke Yahoo Finance
- ❌ API Yahoo Finance membatasi request

## Karakteristik Sample Data

### ✅ Realistis
- Data dibuat menggunakan **random walk with drift** - model matematis yang umum untuk harga saham
- Volatilitas ~1.5% per hari (sesuai dengan saham BBRI)
- Harga berkisar 4200-5800 IDR (range realistis BBRI)
- Volume trading 50-200 juta saham per hari

### ✅ Lengkap
- Data OHLCV (Open, High, Low, Close, Volume)
- Semua indikator teknikal (MA7, MA30, RSI, MACD, Bollinger Bands)
- 240 hari data historis (cukup untuk training)

### ✅ Konsisten
- Menggunakan seed random yang sama untuk reproducibility
- Data yang sama akan dihasilkan setiap kali
- Hanya untuk hari kerja (Senin-Jumat)

## Perbedaan dengan Data Real

| Aspek | Data Real (yfinance) | Sample Data |
|-------|---------------------|-------------|
| **Sumber** | Yahoo Finance API | Generated locally |
| **Akurasi** | 100% real market data | Simulasi realistis |
| **Update** | Real-time | Static (generated once) |
| **Internet** | Required | Not required |
| **Prediksi** | Untuk keputusan real | Untuk demo/testing |

## Cara Mengetahui Mode yang Digunakan

### Di Console Backend
Ketika sample data digunakan, Anda akan melihat pesan:
```
⚠️ Yahoo Finance unavailable. Using SAMPLE DATA for demonstration.
📊 This is realistic BBRI stock data generated for demo purposes.
💡 For real predictions, ensure internet connection and Yahoo Finance access.
✓ Sample data loaded successfully: 240 rows
```

### Di Frontend
*(Akan ditambahkan)* Warning banner akan muncul di atas hasil prediksi.

## Cara Beralih ke Data Real

1. **Pastikan koneksi internet** stabil
2. **Test akses Yahoo Finance** di browser:
   - Buka: https://finance.yahoo.com/quote/BBRI.JK
   - Pastikan data muncul
3. **Restart backend server**
4. **Coba prediksi lagi**

Aplikasi akan otomatis mencoba menggunakan data real terlebih dahulu.

## Kapan Menggunakan Sample Data?

### ✅ Cocok untuk:
- **Demo aplikasi** kepada klien/stakeholder
- **Testing fungsionalitas** tanpa internet
- **Development** fitur baru
- **Presentasi** di tempat tanpa WiFi
- **Training** cara menggunakan aplikasi

### ❌ TIDAK cocok untuk:
- **Keputusan investasi real**
- **Analisis pasar aktual**
- **Backtesting** strategi trading
- **Research** akademik
- **Production deployment**

## Technical Details

### Data Generation Algorithm
```python
# Simplified version
base_price = 5000  # IDR
volatility = 0.015  # 1.5% daily
trend = 0.0002  # Slight upward bias

for each day:
    change = random.normal(trend, volatility)
    new_price = previous_price * (1 + change)
    price = clip(new_price, 4200, 5800)  # Keep in range
```

### Seed Value
```python
np.random.seed(42)  # Fixed seed for reproducibility
```

## FAQ

### Q: Apakah prediksi dengan sample data akurat?
**A:** Tidak untuk keputusan real. Sample data hanya untuk demonstrasi fungsionalitas model, bukan untuk prediksi aktual.

### Q: Bisakah saya mengubah sample data?
**A:** Ya, edit file `backend/predictor/sample_data.py` dan sesuaikan parameter seperti `base_price`, `volatility`, atau `trend`.

### Q: Apakah model TFT tetap digunakan?
**A:** Ya! Model TFT yang sama tetap digunakan untuk prediksi, hanya data inputnya yang berbeda.

### Q: Bagaimana cara memaksa menggunakan data real?
**A:** Tidak ada cara untuk "memaksa". Aplikasi akan selalu mencoba data real terlebih dahulu (3x retry), baru fallback ke sample data jika gagal.

## Troubleshooting

### Sample data juga error
Jika sample data juga gagal, kemungkinan:
- Library `ta` (technical analysis) tidak terinstall
- Library `pandas` atau `numpy` bermasalah
- File `sample_data.py` corrupt

**Solusi:**
```bash
pip install --upgrade ta pandas numpy
```

### Ingin disable sample data fallback
Edit `backend/predictor/model.py`, hapus bagian fallback di fungsi `fetch_and_prepare_data`.

---

## Kesimpulan

Sample Data Mode adalah **safety net** yang memastikan aplikasi tetap bisa digunakan untuk demo dan testing meskipun tanpa akses ke Yahoo Finance. 

**Ingat:** Selalu gunakan data real untuk keputusan investasi aktual!

---

*Last Updated: December 2025*
