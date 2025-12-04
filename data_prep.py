"""
Modul untuk persiapan data dan perhitungan parameter statistik
untuk simulasi Monte Carlo.
"""

import pandas as pd
import numpy as np


def load_data(file_path):
    """
    Memuat data dari file Excel atau CSV.
    
    Parameters:
    -----------
    file_path : str
        Path ke file data (Excel atau CSV)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame yang berisi kolom tahun dan jumlah
    """
    import os
    
    # Cek ekstensi file
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Coba baca sebagai Excel terlebih dahulu jika ekstensi .xlsx atau .xls
    if file_ext in ['.xlsx', '.xls']:
        try:
            # Coba baca semua sheet terlebih dahulu untuk melihat struktur
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            # Coba baca sheet pertama dengan berbagai engine
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_names[0], engine='openpyxl')
            except:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_names[0], engine='xlrd')
                except:
                    df = pd.read_excel(file_path, sheet_name=sheet_names[0])
            
            # Jika sheet pertama kosong atau tidak ada data, coba sheet lain
            if (df.empty or len(df) == 0) and len(sheet_names) > 1:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_names[1], engine='openpyxl')
                except:
                    try:
                        df = pd.read_excel(file_path, sheet_name=sheet_names[1], engine='xlrd')
                    except:
                        df = pd.read_excel(file_path, sheet_name=sheet_names[1])
                
        except Exception as e:
            # Jika gagal, coba sebagai CSV
            try:
                df = pd.read_csv(file_path, sep=',', encoding='utf-8')
            except:
                try:
                    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                    except:
                        # Coba dengan encoding berbeda
                        try:
                            df = pd.read_csv(file_path, sep=',', encoding='latin-1')
                        except:
                            df = pd.read_csv(file_path, sep=';', encoding='latin-1')
    else:
        # File CSV - coba berbagai separator dan encoding
        # Cek versi pandas untuk kompatibilitas
        try:
            pandas_version = pd.__version__
            use_on_bad_lines = int(pandas_version.split('.')[0]) >= 2 or (int(pandas_version.split('.')[0]) == 1 and int(pandas_version.split('.')[1]) >= 4)
        except:
            use_on_bad_lines = False
        
        csv_params = {}
        if use_on_bad_lines:
            csv_params['on_bad_lines'] = 'skip'
        else:
            csv_params['error_bad_lines'] = False
            csv_params['warn_bad_lines'] = False
        
        try:
            df = pd.read_csv(file_path, sep=',', encoding='utf-8', **csv_params)
        except:
            try:
                df = pd.read_csv(file_path, sep=';', encoding='utf-8', **csv_params)
            except:
                try:
                    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', **csv_params)
                except:
                    try:
                        df = pd.read_csv(file_path, sep=',', encoding='latin-1', **csv_params)
                    except:
                        try:
                            df = pd.read_csv(file_path, sep=';', encoding='latin-1', **csv_params)
                        except:
                            # Coba dengan engine python yang lebih toleran
                            try:
                                df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8', **csv_params)
                            except Exception as csv_error:
                                # Jika semua percobaan gagal, raise error
                                raise ValueError(f"Tidak bisa membaca file CSV {file_path}. Error: {str(csv_error)}")
    
    # Pastikan df terdefinisi
    if 'df' not in locals():
        raise ValueError(f"Tidak bisa membaca file {file_path}. Pastikan file adalah Excel (.xlsx, .xls) atau CSV yang valid.")
    
    # Hapus baris kosong
    df = df.dropna(how='all')
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Normalisasi nama kolom (case-insensitive, strip whitespace)
    df.columns = df.columns.str.strip().str.lower()
    
    # Cari kolom yang cocok dengan 'tahun' atau 'year'
    year_cols = [col for col in df.columns if 'tahun' in col or 'year' in col]
    value_cols = [col for col in df.columns if 'jumlah' in col or 'value' in col or 'nilai' in col or 'garis' in col]
    
    if not year_cols:
        # Jika tidak ditemukan, coba kolom pertama yang numerik
        for col in df.columns:
            try:
                pd.to_numeric(df[col].iloc[0])
                if df[col].dtype in ['int64', 'float64'] or df[col].dtype.name.startswith('int') or df[col].dtype.name.startswith('float'):
                    year_cols = [col]
                    break
            except:
                continue
    
    if not value_cols:
        # Jika tidak ditemukan, coba kolom kedua yang numerik
        numeric_cols = []
        for col in df.columns:
            try:
                pd.to_numeric(df[col].iloc[0])
                if df[col].dtype in ['int64', 'float64'] or df[col].dtype.name.startswith('int') or df[col].dtype.name.startswith('float'):
                    numeric_cols.append(col)
            except:
                continue
        
        if len(numeric_cols) >= 2:
            value_cols = [numeric_cols[1]]
        elif len(numeric_cols) == 1 and year_cols and numeric_cols[0] != year_cols[0]:
            value_cols = [numeric_cols[0]]
    
    if year_cols:
        df = df.rename(columns={year_cols[0]: 'tahun'})
    else:
        raise ValueError("Kolom 'tahun' tidak ditemukan dalam data. Kolom yang tersedia: " + str(list(df.columns)))
    
    if value_cols:
        df = df.rename(columns={value_cols[0]: 'jumlah'})
    else:
        raise ValueError("Kolom 'jumlah' tidak ditemukan dalam data. Kolom yang tersedia: " + str(list(df.columns)))
    
    # Pastikan kolom tahun dan jumlah ada dan tidak kosong
    if 'tahun' not in df.columns or 'jumlah' not in df.columns:
        raise ValueError(f"Kolom yang diperlukan tidak ditemukan. Kolom yang tersedia: {list(df.columns)}")
    
    # Hapus baris dengan nilai NaN di kolom penting
    df = df.dropna(subset=['tahun', 'jumlah'])
    
    # Konversi tipe data
    df['tahun'] = pd.to_numeric(df['tahun'], errors='coerce')
    df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce')
    
    # Hapus baris dengan nilai NaN setelah konversi
    df = df.dropna(subset=['tahun', 'jumlah'])
    
    return df


def calculate_log_returns(df, year_col='tahun', value_col='jumlah'):
    """
    Menghitung logarithmic return dari data historis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame yang berisi data historis
    year_col : str
        Nama kolom tahun
    value_col : str
        Nama kolom nilai (Garis Kemiskinan)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame dengan kolom log_returns ditambahkan
    """
    df = df.copy()
    df = df.sort_values(by=year_col)
    
    # Hitung log returns: ln(S_t / S_{t-1})
    df['log_return'] = np.log(df[value_col] / df[value_col].shift(1))
    
    # Hapus baris pertama yang tidak memiliki return
    df = df.dropna(subset=['log_return'])
    
    return df


def calculate_parameters(df, log_return_col='log_return'):
    """
    Menghitung parameter μ (mean) dan σ (volatilitas/standar deviasi)
    dari log returns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame yang berisi log returns
    log_return_col : str
        Nama kolom log return
    
    Returns:
    --------
    tuple
        (mu, sigma) - rata-rata dan standar deviasi dari log returns
    """
    log_returns = df[log_return_col].values
    
    # μ = rata-rata log return
    mu = np.mean(log_returns)
    
    # σ = standar deviasi log return
    sigma = np.std(log_returns, ddof=1)  # ddof=1 untuk sample std dev
    
    return mu, sigma


def prepare_data(file_path, year_col='tahun', value_col='jumlah'):
    """
    Fungsi utama untuk mempersiapkan data dan menghitung parameter.
    
    Parameters:
    -----------
    file_path : str
        Path ke file data
    year_col : str
        Nama kolom tahun
    value_col : str
        Nama kolom nilai
    
    Returns:
    --------
    tuple
        (df_processed, mu, sigma, last_value, last_year)
        - df_processed: DataFrame dengan log returns
        - mu: rata-rata log return
        - sigma: volatilitas
        - last_value: nilai terakhir dari data historis
        - last_year: tahun terakhir dari data historis
    """
    # Muat data
    df = load_data(file_path)
    
    # Hitung log returns
    df_processed = calculate_log_returns(df, year_col, value_col)
    
    # Hitung parameter
    mu, sigma = calculate_parameters(df_processed)
    
    # Ambil nilai dan tahun terakhir
    last_value = df[value_col].iloc[-1]
    last_year = df[year_col].iloc[-1]
    
    return df_processed, mu, sigma, last_value, last_year

