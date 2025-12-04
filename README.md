# Prediksi Garis Kemiskinan Kota Bandung - Monte Carlo Simulation

Aplikasi web berbasis Streamlit untuk memprediksi Garis Kemiskinan di Kota Bandung menggunakan simulasi Monte Carlo dengan metode Geometric Brownian Motion.

## 📋 Deskripsi

Aplikasi ini melakukan prediksi Garis Kemiskinan (dalam Rupiah/Bulan) untuk beberapa tahun ke depan berdasarkan data historis. Metode yang digunakan adalah simulasi Monte Carlo dengan asumsi pergerakan mengikuti Geometric Brownian Motion.

## 🚀 Fitur

- **Analisis Data Historis**: Menghitung logarithmic returns dari data historis
- **Perhitungan Parameter**: Menghitung parameter μ (drift) dan σ (volatilitas) dari log returns
- **Simulasi Monte Carlo**: Menjalankan 10.000 simulasi untuk prediksi 5 tahun ke depan
- **Visualisasi Interaktif**: 
  - Grafik jalur simulasi dengan confidence interval
  - Distribusi hasil prediksi tahun terakhir
- **Statistik Prediksi**: Menampilkan Mean, P5 (percentile 5%), P50 (median), dan P95 (percentile 95%)

## 📦 Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/shidiqpermana/memprediksi-angka-kemiskinan-monte-carlo.git
cd memprediksi-angka-kemiskinan-monte-carlo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Cara Menggunakan

1. Pastikan file data (`garis_kemiskinan_di_kota_bandung.xlsx` atau `.csv`) berada di direktori yang sama dengan `app.py`

2. Jalankan aplikasi Streamlit:
```bash
streamlit run app.py
```

3. Aplikasi akan otomatis terbuka di browser (biasanya di `http://localhost:8501`)

4. Gunakan sidebar untuk mengatur:
   - Jumlah simulasi (default: 10.000)
   - Periode prediksi (default: 5 tahun)
   - Jumlah jalur yang ditampilkan di grafik

## 📁 Struktur Project

```
.
├── app.py                 # Aplikasi Streamlit utama
├── data_prep.py           # Modul untuk persiapan data dan perhitungan parameter
├── monte_carlo.py         # Modul untuk simulasi Monte Carlo
├── requirements.txt       # Dependencies Python
├── .gitignore            # File yang diabaikan oleh Git
└── README.md             # Dokumentasi
```

## 🔧 Requirements

- Python 3.7+
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- openpyxl (untuk membaca file Excel)
- scipy

## 📊 Format Data

File data harus memiliki kolom:
- **tahun** (atau variasi: Tahun, Year)
- **jumlah** (atau variasi: Jumlah, Value, Nilai, Garis Kemiskinan)

Format file yang didukung:
- Excel (.xlsx, .xls)
- CSV (.csv)

## 🧮 Metodologi

### Geometric Brownian Motion

Model yang digunakan untuk simulasi:

```
S(t) = S₀ × exp((μ - 0.5×σ²)×t + σ×W(t))
```

Dimana:
- S₀ = Nilai awal (Garis Kemiskinan terakhir dari data historis)
- μ = Drift parameter (rata-rata log return)
- σ = Volatility parameter (standar deviasi log return)
- W(t) = Wiener process (Brownian motion)

### Langkah-langkah:

1. **Data Preparation**: 
   - Memuat data historis
   - Menghitung logarithmic returns: `ln(S_t / S_{t-1})`

2. **Parameter Calculation**:
   - μ = Mean dari log returns
   - σ = Standard deviation dari log returns

3. **Monte Carlo Simulation**:
   - Generate 10.000 jalur simulasi untuk periode prediksi
   - Setiap jalur menggunakan random shocks dari distribusi normal

4. **Statistik**:
   - Mean: Rata-rata dari semua simulasi
   - P5, P50, P95: Percentiles untuk confidence interval

## 📈 Output

Aplikasi menampilkan:
- **Informasi Data & Parameter**: Tahun terakhir, nilai terakhir, parameter μ dan σ
- **Statistik Prediksi**: Mean, P5, P50, P95 untuk tahun prediksi
- **Visualisasi**:
  - Grafik jalur simulasi dengan mean path dan confidence interval
  - Histogram distribusi hasil akhir dengan KDE curve

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan buat issue atau pull request.

## 📝 License

Project ini bebas digunakan untuk keperluan edukasi dan penelitian.

## 👤 Author

**Shidiq Permana**

## 🙏 Acknowledgments

- Data Garis Kemiskinan Kota Bandung
- Streamlit untuk framework web application
- Python scientific libraries (pandas, numpy, matplotlib)

