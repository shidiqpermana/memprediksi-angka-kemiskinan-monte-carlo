"""
Aplikasi Streamlit untuk prediksi Garis Kemiskinan menggunakan Monte Carlo Simulation.
"""

import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_prep import prepare_data
from monte_carlo import run_monte_carlo_simulation

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Garis Kemiskinan Kota Bandung",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Konfigurasi
POSSIBLE_DATA_FILES = [
    'garis_kemiskinan_di_kota_bandung.xlsx',
    'garis_kemiskinan_di_kota_bandung.csv',
    'data.csv'
]

# Sidebar untuk konfigurasi
st.sidebar.header("⚙️ Konfigurasi Simulasi")

# Input parameter
n_simulations = st.sidebar.slider(
    "Jumlah Simulasi",
    min_value=1000,
    max_value=50000,
    value=10000,
    step=1000,
    help="Semakin banyak simulasi, semakin akurat hasilnya (tapi lebih lambat)"
)

prediction_years = st.sidebar.slider(
    "Periode Prediksi (Tahun)",
    min_value=1,
    max_value=10,
    value=5,
    step=1
)

n_paths_to_show = st.sidebar.slider(
    "Jumlah Jalur yang Ditampilkan",
    min_value=10,
    max_value=500,
    value=100,
    step=10,
    help="Jumlah jalur simulasi yang ditampilkan di grafik"
)

# Header utama
st.markdown('<p class="main-header">📊 Prediksi Garis Kemiskinan Kota Bandung</p>', 
            unsafe_allow_html=True)
st.markdown("### Simulasi Monte Carlo dengan Geometric Brownian Motion")

# File uploader di sidebar
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload file data (Excel atau CSV)",
    type=['xlsx', 'xls', 'csv'],
    help="Upload file data yang berisi kolom 'tahun' dan 'jumlah'"
)

# Cari file data lokal (untuk development)
data_file = None
if uploaded_file is not None:
    # Simpan file yang di-upload ke temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        data_file = tmp_file.name
    st.sidebar.success(f"✅ File di-upload: {uploaded_file.name}")
else:
    # Coba cari file lokal
    for file_path in POSSIBLE_DATA_FILES:
        if os.path.exists(file_path):
            data_file = file_path
            break
    
    if data_file is None:
        st.warning("⚠️ File data tidak ditemukan. Silakan upload file data menggunakan sidebar di sebelah kiri.")
        st.info("""
        **Format file yang didukung:**
        - Excel (.xlsx, .xls)
        - CSV (.csv)
        
        **Kolom yang diperlukan:**
        - `tahun` (atau Tahun, Year)
        - `jumlah` (atau Jumlah, Value, Nilai, Garis Kemiskinan)
        """)
        st.stop()
    else:
        st.sidebar.success(f"✅ File ditemukan: {data_file}")

# Tampilkan progress
with st.spinner('Memuat data dan menjalankan simulasi...'):
    try:
        # Persiapan data dan perhitungan parameter
        try:
            df_processed, mu, sigma, last_value, last_year = prepare_data(
                data_file, 
                year_col='tahun', 
                value_col='jumlah'
            )
            
            # Hapus temporary file jika dari upload
            if uploaded_file is not None and os.path.exists(data_file):
                try:
                    os.unlink(data_file)
                except:
                    pass
        except Exception as prep_error:
            st.error(f"❌ Error saat memproses data: {str(prep_error)}")
            
            # Coba tampilkan preview data untuk debugging
            with st.expander("🔍 Debug: Lihat struktur file"):
                df_preview = None
                try:
                    if data_file.endswith('.xlsx') or data_file.endswith('.xls'):
                        try:
                            df_preview = pd.read_excel(data_file, nrows=10)
                        except Exception as e1:
                            try:
                                df_preview = pd.read_excel(data_file, nrows=10, engine='openpyxl')
                            except Exception as e2:
                                st.write(f"Tidak bisa membaca sebagai Excel: {str(e2)}")
                    else:
                        try:
                            df_preview = pd.read_csv(data_file, nrows=10, sep=',')
                        except:
                            try:
                                df_preview = pd.read_csv(data_file, nrows=10, sep=';')
                            except:
                                try:
                                    df_preview = pd.read_csv(data_file, nrows=10, engine='python')
                                except Exception as e3:
                                    st.write(f"Tidak bisa membaca sebagai CSV: {str(e3)}")
                    
                    if df_preview is not None and not df_preview.empty:
                        st.write("**Preview data (10 baris pertama):**")
                        st.dataframe(df_preview)
                        st.write(f"**Kolom yang ditemukan:** {list(df_preview.columns)}")
                        st.write(f"**Jumlah baris:** {len(df_preview)}")
                    else:
                        st.write("⚠️ Tidak bisa membaca file atau file kosong")
                except Exception as debug_error:
                    st.write(f"Tidak bisa menampilkan preview: {str(debug_error)}")
            
            st.info("💡 Tips: Pastikan file memiliki kolom 'tahun' dan 'jumlah' (atau variasi seperti 'Tahun'/'Year' dan 'Jumlah'/'Value')")
            st.stop()
        
        # Jalankan simulasi Monte Carlo
        simulation_results = run_monte_carlo_simulation(
            S0=last_value,
            mu=mu,
            sigma=sigma,
            n_simulations=n_simulations,
            prediction_years=prediction_years,
            start_year=last_year + 1
        )
        
        statistics = simulation_results['statistics']
        paths = simulation_results['paths']
        years = simulation_results['years']
        final_values = simulation_results['final_values']
        
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {str(e)}")
        st.stop()

# Tampilkan informasi data
st.success("✅ Data berhasil dimuat dan simulasi selesai!")

# Section 1: Informasi Data & Parameter
st.header("📋 Informasi Data & Parameter")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Tahun Data Terakhir", int(last_year))
    
with col2:
    st.metric("Nilai Terakhir", f"Rp {last_value:,.0f}/bulan")
    
with col3:
    st.metric("Tahun Prediksi", int(last_year + prediction_years))
    
with col4:
    st.metric("Periode Prediksi", f"{prediction_years} tahun")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Drift (μ)", f"{mu:.6f}")
    
with col6:
    st.metric("Volatilitas (σ)", f"{sigma:.6f}")
    
with col7:
    st.metric("Jumlah Simulasi", f"{n_simulations:,} jalur")

# Section 2: Statistik Prediksi
st.header("📈 Statistik Prediksi")

prediction_year = int(last_year + prediction_years)

# Tampilkan statistik dalam kolom
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric(
        "Mean (Rata-rata)",
        f"Rp {statistics['Mean']:,.0f}/bulan",
        help="Nilai rata-rata dari semua simulasi"
    )

with stat_col2:
    st.metric(
        "P50 (Median)",
        f"Rp {statistics['P50']:,.0f}/bulan",
        help="Nilai tengah (50% simulasi di bawah nilai ini)"
    )

with stat_col3:
    st.metric(
        "P5 (Percentile 5%)",
        f"Rp {statistics['P5']:,.0f}/bulan",
        help="5% simulasi menghasilkan nilai di bawah ini"
    )

with stat_col4:
    st.metric(
        "P95 (Percentile 95%)",
        f"Rp {statistics['P95']:,.0f}/bulan",
        help="95% simulasi menghasilkan nilai di bawah ini"
    )

# Tabel statistik detail
st.subheader(f"Detail Statistik Prediksi Tahun {prediction_year}")
stats_df = pd.DataFrame({
    'Metrik': ['Mean (Rata-rata)', 'P50 (Median)', 'P5 (Percentile 5%)', 'P95 (Percentile 95%)'],
    'Nilai Prediksi': [
        f"Rp {statistics['Mean']:,.0f}/bulan",
        f"Rp {statistics['P50']:,.0f}/bulan",
        f"Rp {statistics['P5']:,.0f}/bulan",
        f"Rp {statistics['P95']:,.0f}/bulan"
    ],
    'Keterangan': [
        'Nilai rata-rata dari semua simulasi',
        'Nilai tengah (50% simulasi di bawah nilai ini)',
        '5% simulasi menghasilkan nilai di bawah ini',
        '95% simulasi menghasilkan nilai di bawah ini'
    ]
})

st.dataframe(stats_df, use_container_width=True, hide_index=True)

# Section 3: Visualisasi
st.header("📉 Visualisasi Simulasi")

# Plot 1: Jalur Simulasi
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Tampilkan subset jalur
n_paths = min(n_paths_to_show, paths.shape[0])
indices = np.random.choice(paths.shape[0], n_paths, replace=False)

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

ax1.plot(years, p50_path, color='green', linewidth=2, 
         linestyle='--', label=f'Median (P50: {statistics["P50"]:,.0f})')
ax1.fill_between(years, p5_path, p95_path, alpha=0.2, color='gray',
                 label=f'90% Confidence Interval (P5-P95)')

ax1.set_xlabel('Tahun', fontsize=11)
ax1.set_ylabel('Garis Kemiskinan (Rupiah/Bulan)', fontsize=11)
ax1.set_title(f'Jalur Simulasi ({n_paths} dari {paths.shape[0]} jalur)', 
              fontsize=12, fontweight='bold')
ax1.legend(loc='best', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

st.pyplot(fig1)
plt.close(fig1)

# Plot 2: Distribusi Hasil Akhir
fig2, ax2 = plt.subplots(figsize=(12, 6))

# Histogram
ax2.hist(final_values, bins=50, alpha=0.7, color='skyblue', 
         edgecolor='black', density=True)

# Tambahkan garis vertikal untuk statistik
ax2.axvline(statistics['Mean'], color='red', linestyle='-', 
            linewidth=2, label=f"Mean: {statistics['Mean']:,.0f}")
ax2.axvline(statistics['P50'], color='green', linestyle='--', 
            linewidth=2, label=f"Median (P50): {statistics['P50']:,.0f}")
ax2.axvline(statistics['P5'], color='orange', linestyle=':', 
            linewidth=2, label=f"P5: {statistics['P5']:,.0f}")
ax2.axvline(statistics['P95'], color='purple', linestyle=':', 
            linewidth=2, label=f"P95: {statistics['P95']:,.0f}")

# KDE curve
try:
    from scipy import stats
    kde = stats.gaussian_kde(final_values)
    x_range = np.linspace(final_values.min(), final_values.max(), 200)
    ax2.plot(x_range, kde(x_range), color='darkblue', linewidth=2, 
             label='KDE')
except:
    pass

ax2.set_xlabel('Garis Kemiskinan (Rupiah/Bulan)', fontsize=11)
ax2.set_ylabel('Density', fontsize=11)
ax2.set_title('Distribusi Prediksi Tahun Terakhir', fontsize=12, fontweight='bold')
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

st.pyplot(fig2)
plt.close(fig2)

# Section 4: Data Historis (opsional)
with st.expander("📊 Lihat Data Historis"):
    st.subheader("Data Log Returns")
    st.dataframe(df_processed[['tahun', 'jumlah', 'log_return']], use_container_width=True)
    
    # Plot data historis
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(df_processed['tahun'], df_processed['jumlah'], 
             marker='o', linewidth=2, markersize=6, color='#1f77b4')
    ax3.set_xlabel('Tahun', fontsize=11)
    ax3.set_ylabel('Garis Kemiskinan (Rupiah/Bulan)', fontsize=11)
    ax3.set_title('Data Historis Garis Kemiskinan', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    st.pyplot(fig3)
    plt.close(fig3)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Dibuat dengan Python Streamlit & Monte Carlo Simulation | Geometric Brownian Motion"
    "</div>",
    unsafe_allow_html=True
)
