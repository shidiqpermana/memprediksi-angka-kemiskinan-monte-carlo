"""
Modul untuk simulasi Monte Carlo menggunakan Geometric Brownian Motion.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def geometric_brownian_motion(S0, mu, sigma, T, dt, n_simulations):
    """
    Simulasi Geometric Brownian Motion untuk prediksi harga.
    
    Formula: S(t) = S0 * exp((μ - 0.5*σ²)*t + σ*W(t))
    dimana W(t) adalah Wiener process (Brownian motion)
    
    Parameters:
    -----------
    S0 : float
        Nilai awal (harga terakhir dari data historis)
    mu : float
        Drift parameter (rata-rata log return)
    sigma : float
        Volatility parameter (standar deviasi log return)
    T : int
        Periode prediksi (dalam tahun)
    dt : float
        Time step (default: 1 untuk tahunan)
    n_simulations : int
        Jumlah simulasi (path)
    
    Returns:
    --------
    np.ndarray
        Array dengan shape (n_simulations, T+1) berisi semua jalur simulasi
    """
    # Inisialisasi array untuk menyimpan semua jalur
    paths = np.zeros((n_simulations, T + 1))
    paths[:, 0] = S0  # Set nilai awal untuk semua simulasi
    
    # Generate random numbers untuk semua time steps sekaligus
    # Menggunakan vectorization untuk efisiensi
    random_shocks = np.random.normal(0, 1, (n_simulations, T))
    
    # Simulasi untuk setiap time step
    for t in range(1, T + 1):
        # Geometric Brownian Motion formula
        # S(t) = S(t-1) * exp((μ - 0.5*σ²)*dt + σ*√dt*Z)
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * random_shocks[:, t-1]
        paths[:, t] = paths[:, t-1] * np.exp(drift + diffusion)
    
    return paths


def run_monte_carlo_simulation(S0, mu, sigma, n_simulations=10000, 
                                prediction_years=5, start_year=None):
    """
    Menjalankan simulasi Monte Carlo lengkap.
    
    Parameters:
    -----------
    S0 : float
        Nilai awal (harga terakhir)
    mu : float
        Drift parameter
    sigma : float
        Volatility parameter
    n_simulations : int
        Jumlah simulasi (default: 10000)
    prediction_years : int
        Periode prediksi dalam tahun (default: 5)
    start_year : int
        Tahun awal prediksi (optional)
    
    Returns:
    --------
    dict
        Dictionary berisi:
        - 'paths': array simulasi paths
        - 'years': array tahun prediksi
        - 'final_values': nilai akhir dari setiap simulasi
        - 'statistics': dict dengan Mean, P5, P50, P95
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


def plot_simulation_paths(simulation_results, n_paths_to_show=100):
    """
    Membuat plot jalur simulasi dan distribusi hasil akhir.
    
    Parameters:
    -----------
    simulation_results : dict
        Hasil dari run_monte_carlo_simulation
    n_paths_to_show : int
        Jumlah jalur yang ditampilkan di plot (default: 100)
    
    Returns:
    --------
    str
        Base64 encoded string dari gambar plot
    """
    paths = simulation_results['paths']
    years = simulation_results['years']
    final_values = simulation_results['final_values']
    statistics = simulation_results['statistics']
    
    # Setup figure dengan 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Simulasi Monte Carlo - Prediksi Garis Kemiskinan Kota Bandung', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: Jalur Simulasi
    ax1 = axes[0]
    
    # Tampilkan subset jalur untuk visualisasi yang lebih jelas
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
                  fontsize=12)
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Format y-axis dengan separator ribuan
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Plot 2: Distribusi Hasil Akhir
    ax2 = axes[1]
    
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
    from scipy import stats
    try:
        kde = stats.gaussian_kde(final_values)
        x_range = np.linspace(final_values.min(), final_values.max(), 200)
        ax2.plot(x_range, kde(x_range), color='darkblue', linewidth=2, 
                 label='KDE')
    except:
        pass
    
    ax2.set_xlabel('Garis Kemiskinan (Rupiah/Bulan)', fontsize=11)
    ax2.set_ylabel('Density', fontsize=11)
    ax2.set_title('Distribusi Prediksi Tahun Terakhir', fontsize=12)
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis dengan separator ribuan
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str

