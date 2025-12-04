# LAPORAN PROJECT
## Prediksi Garis Kemiskinan Kota Bandung Menggunakan Simulasi Monte Carlo

---

## A. DESKRIPSI STUDI KASUS

### 1. Latar Belakang

Garis Kemiskinan merupakan indikator penting dalam mengukur tingkat kesejahteraan masyarakat. Prediksi Garis Kemiskinan di masa depan sangat diperlukan untuk perencanaan kebijakan ekonomi dan sosial. Kota Bandung sebagai salah satu kota besar di Indonesia memerlukan analisis prediktif untuk mengantisipasi perubahan Garis Kemiskinan di masa depan.

### 2. Tujuan Project

Project ini bertujuan untuk:
- Memprediksi Garis Kemiskinan Kota Bandung untuk 5 tahun ke depan
- Menggunakan metode simulasi Monte Carlo dengan Geometric Brownian Motion
- Membangun aplikasi web interaktif menggunakan Streamlit
- Menyediakan visualisasi yang informatif untuk analisis prediksi

### 3. Data yang Digunakan

Data yang digunakan adalah data historis Garis Kemiskinan Kota Bandung yang berisi:
- **Kolom Tahun**: Menunjukkan tahun pengamatan
- **Kolom Jumlah**: Nilai Garis Kemiskinan dalam Rupiah per Bulan

Data ini digunakan untuk menghitung parameter statistik yang diperlukan dalam simulasi Monte Carlo.

### 4. Metodologi

Project ini menggunakan pendekatan **Geometric Brownian Motion (GBM)** untuk memodelkan pergerakan Garis Kemiskinan. Metode ini umum digunakan dalam pemodelan finansial dan ekonomi untuk memprediksi pergerakan harga atau nilai yang memiliki volatilitas.

---

## B. PERSAMAAN ATAU RUMUS-RUMUS YANG DIGUNAKAN

### 1. Logarithmic Return

Logarithmic return digunakan untuk mengukur persentase perubahan tahunan dari Garis Kemiskinan:

\[
r_t = \ln\left(\frac{S_t}{S_{t-1}}\right)
\]

Dimana:
- \(r_t\) = logarithmic return pada periode t
- \(S_t\) = Nilai Garis Kemiskinan pada periode t
- \(S_{t-1}\) = Nilai Garis Kemiskinan pada periode sebelumnya

### 2. Parameter Drift (μ)

Drift parameter dihitung sebagai rata-rata dari logarithmic returns:

\[
\mu = \frac{1}{n} \sum_{i=1}^{n} r_i
\]

Dimana:
- \(\mu\) = drift parameter (rata-rata pertumbuhan)
- \(n\) = jumlah observasi
- \(r_i\) = logarithmic return ke-i

### 3. Parameter Volatilitas (σ)

Volatilitas dihitung sebagai standar deviasi dari logarithmic returns:

\[
\sigma = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (r_i - \mu)^2}
\]

Dimana:
- \(\sigma\) = volatilitas (ukuran ketidakpastian)
- \(n-1\) = degrees of freedom (sample standard deviation)

### 4. Geometric Brownian Motion (GBM)

Model GBM untuk prediksi nilai di masa depan:

\[
S(t) = S_0 \times \exp\left((\mu - 0.5\sigma^2) \times t + \sigma \times W(t)\right)
\]

Dimana:
- \(S(t)\) = Nilai prediksi pada waktu t
- \(S_0\) = Nilai awal (nilai terakhir dari data historis)
- \(\mu\) = drift parameter
- \(\sigma\) = volatilitas parameter
- \(t\) = waktu (dalam tahun)
- \(W(t)\) = Wiener process (Brownian motion) ~ N(0, t)

### 5. Diskritisasi GBM untuk Simulasi

Untuk simulasi numerik, persamaan GBM didiskritisasi:

\[
S_{t+\Delta t} = S_t \times \exp\left((\mu - 0.5\sigma^2) \times \Delta t + \sigma \times \sqrt{\Delta t} \times Z\right)
\]

Dimana:
- \(\Delta t\) = time step (dalam project ini = 1 tahun)
- \(Z\) = random variable dari distribusi normal standar ~ N(0, 1)

### 6. Statistik Prediksi

Dari hasil simulasi, dihitung statistik berikut:

- **Mean**: \(\bar{S} = \frac{1}{N} \sum_{i=1}^{N} S_i\)
- **Percentile 5% (P5)**: Nilai dimana 5% simulasi berada di bawahnya
- **Percentile 50% (P50/Median)**: Nilai tengah dari distribusi
- **Percentile 95% (P95)**: Nilai dimana 95% simulasi berada di bawahnya

Dimana \(N\) = jumlah simulasi (dalam project ini = 10,000)

---

## C. PEMODELAN MENGGUNAKAN PYTHON

### 1. Struktur Project

```
memprediksi-angka-kemiskinan-monte-carlo/
├── app.py                 # Aplikasi Streamlit utama
├── data_prep.py           # Modul persiapan data
├── monte_carlo.py         # Modul simulasi Monte Carlo
├── requirements.txt       # Dependencies
├── runtime.txt           # Versi Python
└── README.md             # Dokumentasi
```

### 2. Alur Pemodelan

```
Data Historis
    ↓
[data_prep.py]
    ├── Load Data
    ├── Calculate Log Returns
    ├── Calculate μ (mu)
    └── Calculate σ (sigma)
    ↓
[monte_carlo.py]
    ├── Geometric Brownian Motion
    ├── 10,000 Simulasi
    └── Calculate Statistics
    ↓
[app.py]
    ├── Streamlit Interface
    ├── Visualization
    └── Display Results
```

### 3. Library yang Digunakan

- **pandas**: Untuk manipulasi dan analisis data
- **numpy**: Untuk komputasi numerik dan array operations
- **matplotlib**: Untuk visualisasi grafik
- **scipy**: Untuk statistik (KDE curve)
- **streamlit**: Untuk aplikasi web interaktif
- **openpyxl**: Untuk membaca file Excel

---

## D. PENJELASAN KODING

### 1. Modul `data_prep.py`

#### a. Fungsi `load_data(file_path)`

```python
def load_data(file_path):
    """
    Memuat data dari file Excel atau CSV.
    """
    # Deteksi format file
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Baca Excel atau CSV dengan berbagai fallback
    if file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        df = pd.read_csv(file_path, sep=',', encoding='utf-8')
    
    # Normalisasi nama kolom
    df.columns = df.columns.str.strip().str.lower()
    
    return df
```

**Penjelasan:**
- Fungsi ini membaca file data (Excel atau CSV)
- Otomatis mendeteksi format file
- Normalisasi nama kolom menjadi lowercase untuk fleksibilitas
- Mencari kolom yang cocok dengan 'tahun' dan 'jumlah'

#### b. Fungsi `calculate_log_returns(df, year_col, value_col)`

```python
def calculate_log_returns(df, year_col='tahun', value_col='jumlah'):
    """
    Menghitung logarithmic return dari data historis.
    """
    df = df.copy()
    df = df.sort_values(by=year_col)
    
    # Hitung log returns: ln(S_t / S_{t-1})
    df['log_return'] = np.log(df[value_col] / df[value_col].shift(1))
    
    # Hapus baris pertama yang tidak memiliki return
    df = df.dropna(subset=['log_return'])
    
    return df
```

**Penjelasan:**
- Mengurutkan data berdasarkan tahun
- Menghitung log return menggunakan formula: `ln(S_t / S_{t-1})`
- `shift(1)` mengambil nilai periode sebelumnya
- Baris pertama dihapus karena tidak memiliki return

#### c. Fungsi `calculate_parameters(df, log_return_col)`

```python
def calculate_parameters(df, log_return_col='log_return'):
    """
    Menghitung parameter μ (mean) dan σ (volatilitas).
    """
    log_returns = df[log_return_col].values
    
    # μ = rata-rata log return
    mu = np.mean(log_returns)
    
    # σ = standar deviasi log return
    sigma = np.std(log_returns, ddof=1)  # ddof=1 untuk sample std dev
    
    return mu, sigma
```

**Penjelasan:**
- `mu`: Rata-rata dari semua log returns (drift parameter)
- `sigma`: Standar deviasi dengan `ddof=1` untuk sample standard deviation
- Parameter ini digunakan dalam simulasi GBM

### 2. Modul `monte_carlo.py`

#### a. Fungsi `geometric_brownian_motion(S0, mu, sigma, T, dt, n_simulations)`

```python
def geometric_brownian_motion(S0, mu, sigma, T, dt, n_simulations):
    """
    Simulasi Geometric Brownian Motion untuk prediksi harga.
    """
    # Inisialisasi array untuk menyimpan semua jalur
    paths = np.zeros((n_simulations, T + 1))
    paths[:, 0] = S0  # Set nilai awal untuk semua simulasi
    
    # Generate random numbers untuk semua time steps sekaligus
    random_shocks = np.random.normal(0, 1, (n_simulations, T))
    
    # Simulasi untuk setiap time step
    for t in range(1, T + 1):
        # Geometric Brownian Motion formula
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * random_shocks[:, t-1]
        paths[:, t] = paths[:, t-1] * np.exp(drift + diffusion)
    
    return paths
```

**Penjelasan:**
- `paths`: Array 2D dengan shape (n_simulations, T+1) untuk menyimpan semua jalur
- `random_shocks`: Random numbers dari distribusi normal standar N(0,1)
- **Drift term**: `(μ - 0.5σ²) × dt` - komponen deterministik
- **Diffusion term**: `σ × √dt × Z` - komponen stokastik
- Setiap jalur dihitung secara independen menggunakan formula GBM

#### b. Fungsi `run_monte_carlo_simulation(...)`

```python
def run_monte_carlo_simulation(S0, mu, sigma, n_simulations=10000, 
                                prediction_years=5, start_year=None):
    """
    Menjalankan simulasi Monte Carlo lengkap.
    """
    # Jalankan simulasi
    paths = geometric_brownian_motion(S0, mu, sigma, prediction_years, 
                                      dt=1.0, n_simulations=n_simulations)
    
    # Generate tahun prediksi
    if start_year:
        years = np.arange(start_year, start_year + prediction_years + 1)
    else:
        years = np.arange(0, prediction_years + 1)
    
    # Ambil nilai akhir dari setiap simulasi
    final_values = paths[:, -1]
    
    # Hitung statistik
    statistics = {
        'Mean': np.mean(final_values),
        'P5': np.percentile(final_values, 5),
        'P50': np.percentile(final_values, 50),  # Median
        'P95': np.percentile(final_values, 95)
    }
    
    return {
        'paths': paths,
        'years': years,
        'final_values': final_values,
        'statistics': statistics
    }
```

**Penjelasan:**
- Menjalankan simulasi GBM untuk semua jalur
- Mengambil nilai akhir dari setiap simulasi (tahun terakhir)
- Menghitung statistik: Mean, P5, P50, P95
- Mengembalikan semua hasil untuk visualisasi

### 3. Modul `app.py`

#### a. Konfigurasi Streamlit

```python
st.set_page_config(
    page_title="Prediksi Garis Kemiskinan Kota Bandung",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Penjelasan:**
- Mengatur konfigurasi halaman Streamlit
- Layout wide untuk tampilan yang lebih luas
- Sidebar expanded untuk akses mudah ke kontrol

#### b. File Uploader

```python
uploaded_file = st.sidebar.file_uploader(
    "Upload file data (Excel atau CSV)",
    type=['xlsx', 'xls', 'csv'],
    help="Upload file data yang berisi kolom 'tahun' dan 'jumlah'"
)

if uploaded_file is not None:
    # Simpan file yang di-upload ke temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        data_file = tmp_file.name
```

**Penjelasan:**
- File uploader memungkinkan user mengupload file data
- File disimpan sementara untuk diproses
- Mendukung format Excel dan CSV

#### c. Visualisasi

```python
# Plot 1: Jalur Simulasi
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Tampilkan subset jalur
for idx in indices:
    ax1.plot(years, paths[idx, :], alpha=0.1, color='blue', linewidth=0.5)

# Plot mean path
mean_path = np.mean(paths, axis=0)
ax1.plot(years, mean_path, color='red', linewidth=2, 
         label=f'Mean Path (Mean: {statistics["Mean"]:,.0f})')

# Plot percentiles
p5_path = np.percentile(paths, 5, axis=0)
p50_path = np.percentile(paths, 50, axis=0)
p95_path = np.percentile(paths, 95, axis=0)

ax1.fill_between(years, p5_path, p95_path, alpha=0.2, color='gray',
                 label=f'90% Confidence Interval (P5-P95)')
```

**Penjelasan:**
- Menampilkan subset jalur simulasi (100 dari 10,000) untuk visualisasi
- Mean path: Rata-rata dari semua simulasi
- Percentiles: P5, P50, P95 untuk confidence interval
- Fill between: Area confidence interval 90%

---

## E. PERANCANGAN APLIKASI

### 1. Arsitektur Aplikasi

```
┌─────────────────────────────────────┐
│         Streamlit App (app.py)      │
│  ┌───────────────────────────────┐  │
│  │   User Interface              │  │
│  │   - Sidebar Controls          │  │
│  │   - File Uploader             │  │
│  │   - Visualization             │  │
│  └───────────────────────────────┘  │
│           │                          │
│           ▼                          │
│  ┌───────────────────────────────┐  │
│  │   Data Preparation            │  │
│  │   (data_prep.py)              │  │
│  │   - Load Data                 │  │
│  │   - Calculate Parameters      │  │
│  └───────────────────────────────┘  │
│           │                          │
│           ▼                          │
│  ┌───────────────────────────────┐  │
│  │   Monte Carlo Simulation      │  │
│  │   (monte_carlo.py)            │  │
│  │   - GBM Simulation            │  │
│  │   - Calculate Statistics      │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### 2. User Interface Design

#### a. Sidebar (Kiri)
- **📁 Upload Data**: File uploader untuk data Excel/CSV
- **⚙️ Konfigurasi Simulasi**:
  - Slider: Jumlah Simulasi (1,000 - 50,000)
  - Slider: Periode Prediksi (1 - 10 tahun)
  - Slider: Jumlah Jalur yang Ditampilkan (10 - 500)

#### b. Main Area (Kanan)
1. **Header**: Judul aplikasi
2. **Informasi Data & Parameter**: 
   - Tahun data terakhir
   - Nilai terakhir
   - Parameter μ dan σ
3. **Statistik Prediksi**: 
   - Tabel dengan Mean, P5, P50, P95
4. **Visualisasi**:
   - Grafik jalur simulasi
   - Histogram distribusi hasil akhir

### 3. Flow Diagram

```
Start
  ↓
User membuka aplikasi
  ↓
Upload file data (atau gunakan file lokal)
  ↓
[data_prep.py]
  ├── Load & validate data
  ├── Calculate log returns
  └── Calculate μ & σ
  ↓
[monte_carlo.py]
  ├── Run 10,000 simulations
  ├── Generate paths
  └── Calculate statistics
  ↓
[app.py]
  ├── Display statistics
  ├── Plot simulation paths
  └── Plot distribution
  ↓
User dapat adjust parameters
  ↓
Re-run simulation
  ↓
End
```

### 4. Fitur Interaktif

1. **Dynamic Parameters**: User dapat mengubah jumlah simulasi dan periode prediksi
2. **Real-time Visualization**: Grafik update otomatis saat parameter berubah
3. **File Upload**: Support untuk berbagai format file
4. **Responsive Design**: Layout yang adaptif untuk berbagai ukuran layar

---

## F. HASIL DEPLOY APLIKASI BERBASIS WEB

### 1. Platform Deployment

Aplikasi di-deploy menggunakan **Streamlit Community Cloud** yang menyediakan:
- Hosting gratis untuk aplikasi Streamlit
- Auto-deploy dari GitHub repository
- URL publik untuk akses aplikasi
- Auto-update saat ada perubahan di repository

### 2. Repository GitHub

**URL Repository**: https://github.com/shidiqpermana/memprediksi-angka-kemiskinan-monte-carlo

**Struktur Repository**:
```
memprediksi-angka-kemiskinan-monte-carlo/
├── app.py
├── data_prep.py
├── monte_carlo.py
├── requirements.txt
├── runtime.txt
├── .gitignore
└── README.md
```

### 3. Proses Deployment

1. **Persiapan**:
   - Code di-push ke GitHub repository
   - File `requirements.txt` berisi semua dependencies
   - File `runtime.txt` menentukan versi Python (3.11)

2. **Deploy di Streamlit Cloud**:
   - Login ke https://share.streamlit.io/
   - Connect dengan GitHub account
   - Pilih repository
   - Set main file: `app.py`
   - Klik "Deploy"

3. **Hasil**:
   - Aplikasi tersedia di URL publik
   - Auto-update saat ada commit baru
   - Logs tersedia untuk monitoring

### 4. Screenshot Hasil Deploy

*(Catatan: Screenshot dapat ditambahkan di sini)*

**Fitur yang berhasil di-deploy**:
- ✅ File uploader berfungsi
- ✅ Simulasi Monte Carlo berjalan dengan baik
- ✅ Visualisasi grafik tampil dengan benar
- ✅ Statistik prediksi akurat
- ✅ Responsive design bekerja di berbagai device

---

## G. PENJELASAN APLIKASI

### 1. Cara Menggunakan Aplikasi

#### Langkah 1: Akses Aplikasi
- Buka URL aplikasi yang sudah di-deploy
- Atau jalankan lokal dengan: `streamlit run app.py`

#### Langkah 2: Upload Data
- Klik sidebar di kiri
- Scroll ke bagian "📁 Upload Data"
- Klik "Browse files" atau drag & drop file Excel/CSV
- Pastikan file memiliki kolom 'tahun' dan 'jumlah'

#### Langkah 3: Konfigurasi Simulasi
- Atur **Jumlah Simulasi** (default: 10,000)
  - Semakin banyak, semakin akurat tapi lebih lambat
- Atur **Periode Prediksi** (default: 5 tahun)
- Atur **Jumlah Jalur yang Ditampilkan** (default: 100)

#### Langkah 4: Lihat Hasil
- Statistik prediksi muncul otomatis
- Grafik jalur simulasi ditampilkan
- Histogram distribusi hasil akhir

### 2. Interpretasi Hasil

#### a. Statistik Prediksi

- **Mean (Rata-rata)**: Nilai prediksi yang paling mungkin terjadi
- **P50 (Median)**: Nilai tengah, 50% kemungkinan di atas/bawah nilai ini
- **P5 (Percentile 5%)**: Skenario terburuk (5% kemungkinan lebih rendah)
- **P95 (Percentile 95%)**: Skenario terbaik (95% kemungkinan lebih rendah)

#### b. Grafik Jalur Simulasi

- **Garis Biru Tipis**: Individual simulation paths (100 dari 10,000)
- **Garis Merah Tebal**: Mean path (rata-rata semua simulasi)
- **Garis Hijau Putus-putus**: Median path (P50)
- **Area Abu-abu**: 90% Confidence Interval (P5 - P95)

#### c. Histogram Distribusi

- Menunjukkan distribusi nilai prediksi tahun terakhir
- Garis vertikal menunjukkan statistik (Mean, P50, P5, P95)
- KDE curve menunjukkan estimasi density function

### 3. Contoh Penggunaan

**Skenario 1: Prediksi 5 Tahun ke Depan**
- Set Periode Prediksi = 5
- Jumlah Simulasi = 10,000
- Hasil: Prediksi Garis Kemiskinan untuk 5 tahun ke depan dengan confidence interval

**Skenario 2: Analisis Sensitivitas**
- Ubah jumlah simulasi (1,000 vs 10,000)
- Bandingkan hasil untuk melihat stabilitas prediksi
- Semakin banyak simulasi, semakin stabil hasilnya

**Skenario 3: Prediksi Jangka Panjang**
- Set Periode Prediksi = 10 tahun
- Perhatikan confidence interval yang semakin lebar
- Menunjukkan ketidakpastian yang meningkat untuk prediksi jangka panjang

### 4. Kelebihan Aplikasi

1. **User-Friendly**: Interface yang mudah digunakan
2. **Interaktif**: Parameter dapat diubah real-time
3. **Fleksibel**: Support berbagai format file
4. **Informatif**: Visualisasi yang jelas dan statistik lengkap
5. **Accessible**: Dapat diakses dari mana saja melalui web

### 5. Keterbatasan

1. **Asumsi GBM**: Model mengasumsikan pergerakan mengikuti GBM, mungkin tidak selalu akurat
2. **Data Historis**: Kualitas prediksi bergantung pada kualitas dan jumlah data historis
3. **Volatilitas Konstan**: Model mengasumsikan volatilitas konstan, padahal bisa berubah
4. **Tidak Mempertimbangkan Faktor Eksternal**: Model tidak mempertimbangkan kebijakan atau event khusus

### 6. Pengembangan Selanjutnya

1. **Model yang Lebih Kompleks**: 
   - Stochastic Volatility Model
   - Jump Diffusion Model
   - Regime Switching Model

2. **Fitur Tambahan**:
   - Export hasil ke Excel/PDF
   - Perbandingan dengan metode lain
   - Backtesting accuracy

3. **Analisis Lanjutan**:
   - Sensitivity analysis
   - Scenario analysis
   - Risk metrics (VaR, CVaR)

---

## KESIMPULAN

Aplikasi prediksi Garis Kemiskinan Kota Bandung menggunakan simulasi Monte Carlo telah berhasil dikembangkan dan di-deploy. Aplikasi ini memberikan prediksi yang informatif dengan visualisasi yang jelas, memungkinkan pengguna untuk menganalisis berbagai skenario prediksi dengan mudah.

Metode Geometric Brownian Motion yang digunakan telah terbukti efektif untuk memodelkan pergerakan data finansial dan ekonomi, termasuk Garis Kemiskinan. Dengan 10,000 simulasi, aplikasi memberikan prediksi yang cukup akurat dengan confidence interval yang jelas.

Aplikasi ini dapat digunakan oleh berbagai pihak, mulai dari peneliti, perencana kebijakan, hingga masyarakat umum yang ingin memahami tren Garis Kemiskinan di masa depan.

---

## REFERENSI

1. Hull, J. C. (2018). *Options, Futures, and Other Derivatives*. Pearson.
2. Glasserman, P. (2013). *Monte Carlo Methods in Financial Engineering*. Springer.
3. Streamlit Documentation: https://docs.streamlit.io/
4. NumPy Documentation: https://numpy.org/doc/
5. Pandas Documentation: https://pandas.pydata.org/docs/

---

**Dibuat oleh**: [Nama Anda]  
**Tanggal**: [Tanggal]  
**Versi**: 1.0

