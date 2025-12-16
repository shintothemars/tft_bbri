# 🎯 Panduan Lengkap Pengguna

## Untuk Pengguna Awam (Non-Teknis)

### Apa itu Aplikasi Ini?

Aplikasi ini membantu Anda memprediksi harga saham Bank Rakyat Indonesia (BBRI) menggunakan teknologi Artificial Intelligence (AI). Anda bisa melihat perkiraan harga saham di masa depan beserta visualisasi yang mudah dipahami.

---

## Cara Menggunakan Aplikasi

### Langkah 1: Buka Aplikasi
1. Buka browser (Chrome, Firefox, Edge, dll)
2. Ketik alamat: `http://localhost:3000`
3. Anda akan melihat halaman utama aplikasi

### Langkah 2: Pilih Tanggal Target
1. Pilih **Hari** (1-31)
2. Pilih **Bulan** (Januari-Desember)
3. Pilih **Tahun** (tahun sekarang atau tahun depan)

**Catatan:** Tanggal yang dipilih harus di masa depan, maksimal 30 hari dari data terakhir.

### Langkah 3: Klik Tombol Prediksi
1. Klik tombol **"🔮 Prediksi Sekarang"**
2. Tunggu beberapa detik (biasanya 5-10 detik)
3. Aplikasi akan memproses data dan menampilkan hasil

### Langkah 4: Membaca Hasil Prediksi

Hasil prediksi terdiri dari beberapa bagian:

#### A. Statistik Utama
- **Harga Terakhir**: Harga saham BBRI terakhir yang tercatat
- **Prediksi Harga**: Perkiraan harga di tanggal yang Anda pilih
- **Perubahan**: Naik atau turun berapa persen
- **Rentang Prediksi**: Kemungkinan harga terendah dan tertinggi

#### B. Grafik Interaktif
- **Garis Gelap**: Data harga saham 90 hari terakhir
- **Garis Merah**: Prediksi harga ke depan
- **Area Biru Transparan**: Rentang kemungkinan harga (area ketidakpastian)

**Cara Menggunakan Grafik:**
- Arahkan kursor ke grafik untuk melihat detail harga dan tanggal
- Gunakan scroll mouse untuk zoom in/out
- Klik dan drag untuk menggeser grafik

#### C. Analisis Prediksi
Bagian ini menjelaskan hasil prediksi dalam bahasa yang mudah dipahami, contoh:
> "Berdasarkan model AI, harga saham BBRI diprediksi akan NAIK sebesar 2.5% dalam 7 hari ke depan (dari Rp 5,150 menjadi Rp 5,280)."

---

## Memahami Hasil Prediksi

### Apa itu "Rentang Prediksi"?

Rentang prediksi adalah perkiraan harga terendah dan tertinggi yang mungkin terjadi. Ini menunjukkan tingkat ketidakpastian prediksi.

**Contoh:**
- Prediksi Harga: Rp 5,280
- Rentang: Rp 5,180 - Rp 5,380

Artinya: Harga kemungkinan besar akan berada di antara Rp 5,180 dan Rp 5,380.

### Apa itu "Area Biru" di Grafik?

Area biru transparan di grafik menunjukkan **rentang ketidakpastian**. Semakin lebar area ini, semakin besar ketidakpastian prediksi.

### Apakah Prediksi Ini 100% Akurat?

**TIDAK.** Prediksi ini dibuat menggunakan AI berdasarkan data historis, tetapi:
- Harga saham dipengaruhi banyak faktor (ekonomi, politik, sentimen pasar, dll)
- Tidak ada model yang bisa memprediksi dengan 100% akurat
- Gunakan prediksi ini sebagai **referensi**, bukan keputusan final

---

## Tips Menggunakan Aplikasi

### ✅ DO (Lakukan)
- Gunakan prediksi sebagai salah satu pertimbangan
- Bandingkan dengan analisis lain
- Perhatikan rentang prediksi (confidence interval)
- Cek prediksi secara berkala untuk update terbaru

### ❌ DON'T (Jangan)
- Jangan mengandalkan prediksi 100%
- Jangan investasi hanya berdasarkan prediksi ini
- Jangan panik jika prediksi meleset
- Jangan lupa konsultasi dengan ahli keuangan

---

## FAQ (Pertanyaan Sering Diajukan)

### Q: Dari mana data harga saham diambil?
**A:** Data diambil secara real-time dari Yahoo Finance, sumber data keuangan terpercaya.

### Q: Berapa lama proses prediksi?
**A:** Biasanya 5-10 detik, tergantung kecepatan internet dan komputer Anda.

### Q: Kenapa tidak bisa prediksi lebih dari 30 hari?
**A:** Semakin jauh prediksi, semakin rendah akurasinya. Model dibatasi 30 hari untuk menjaga kualitas prediksi.

### Q: Apa itu Temporal Fusion Transformer (TFT)?
**A:** TFT adalah model AI canggih yang dirancang khusus untuk prediksi data time series (seperti harga saham). Model ini bisa menangkap pola kompleks dalam data historis.

### Q: Apakah aplikasi ini gratis?
**A:** Ya, aplikasi ini gratis untuk digunakan.

### Q: Apakah data saya aman?
**A:** Ya, aplikasi ini tidak menyimpan data pribadi Anda. Semua prediksi dilakukan secara real-time tanpa menyimpan informasi pengguna.

### Q: Bisa prediksi saham lain selain BBRI?
**A:** Saat ini aplikasi hanya untuk BBRI. Untuk saham lain, model perlu dilatih ulang dengan data saham tersebut.

### Q: Kenapa prediksi berbeda setiap hari?
**A:** Prediksi diperbarui dengan data terbaru setiap kali Anda menggunakan aplikasi. Data baru bisa mengubah hasil prediksi.

---

## Troubleshooting (Mengatasi Masalah)

### Masalah: Aplikasi tidak bisa dibuka
**Solusi:**
1. Pastikan backend dan frontend sudah running
2. Cek alamat URL: `http://localhost:3000`
3. Coba refresh browser (F5)
4. Coba browser lain

### Masalah: Tombol prediksi tidak berfungsi
**Solusi:**
1. Pastikan tanggal yang dipilih valid
2. Pastikan tanggal di masa depan
3. Cek koneksi internet
4. Refresh halaman dan coba lagi

### Masalah: Grafik tidak muncul
**Solusi:**
1. Tunggu beberapa detik (loading)
2. Refresh halaman
3. Clear cache browser
4. Coba browser lain

### Masalah: Error "Prediction horizon exceeds maximum"
**Solusi:**
Tanggal yang Anda pilih terlalu jauh. Pilih tanggal yang lebih dekat (maksimal 30 hari dari data terakhir).

---

## Istilah-Istilah Penting

| Istilah | Penjelasan |
|---------|------------|
| **Harga Penutupan (Close)** | Harga saham saat pasar tutup |
| **Prediksi (Prediction)** | Perkiraan harga di masa depan |
| **Median** | Nilai tengah dari prediksi |
| **Confidence Interval** | Rentang kemungkinan harga |
| **Tren (Trend)** | Arah pergerakan harga (naik/turun) |
| **Volatilitas** | Tingkat perubahan harga |
| **Time Series** | Data yang berurutan berdasarkan waktu |

---

## Contoh Kasus Penggunaan

### Skenario 1: Investor Pemula
**Tujuan:** Ingin tahu apakah harga BBRI akan naik minggu depan

**Langkah:**
1. Pilih tanggal 7 hari dari sekarang
2. Klik prediksi
3. Lihat hasil: "Prediksi NAIK 2.5%"
4. Lihat rentang prediksi untuk estimasi risiko
5. Bandingkan dengan analisis lain sebelum membeli

### Skenario 2: Trader Harian
**Tujuan:** Monitoring tren jangka pendek

**Langkah:**
1. Cek prediksi setiap hari
2. Perhatikan perubahan tren
3. Gunakan grafik untuk melihat pola
4. Kombinasikan dengan indikator teknikal lain

### Skenario 3: Investor Jangka Panjang
**Tujuan:** Evaluasi timing entry/exit

**Langkah:**
1. Cek prediksi 30 hari ke depan
2. Lihat tren jangka menengah
3. Perhatikan rentang prediksi (risiko)
4. Gunakan sebagai salah satu faktor keputusan

---

## Disclaimer & Peringatan

⚠️ **PENTING - HARAP DIBACA**

1. **Bukan Saran Investasi**: Aplikasi ini adalah alat bantu analisis, BUKAN saran investasi profesional.

2. **Risiko Investasi**: Investasi saham memiliki risiko. Anda bisa kehilangan sebagian atau seluruh modal.

3. **Akurasi Tidak Dijamin**: Prediksi bisa meleset. Jangan investasi hanya berdasarkan prediksi ini.

4. **Konsultasi Profesional**: Selalu konsultasi dengan financial advisor sebelum membuat keputusan investasi besar.

5. **Tanggung Jawab Pribadi**: Keputusan investasi adalah tanggung jawab Anda sendiri.

---

## Kontak & Dukungan

Jika Anda mengalami masalah atau memiliki pertanyaan:
1. Baca FAQ di atas
2. Cek dokumentasi teknis (README.md)
3. Hubungi administrator sistem

---

**Selamat menggunakan aplikasi prediksi saham BBRI! 📈**

*Investasi cerdas dimulai dengan informasi yang tepat.*
