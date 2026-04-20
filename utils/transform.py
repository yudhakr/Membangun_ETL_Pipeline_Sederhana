import pandas as pd
import numpy as np
from datetime import datetime

toRP = 16000

def ubah_tipedata(df):
    """Mengubah tipe data kolom DataFrame."""
    df['rating'] = df['rating'].astype(float)
    df['colors'] = df['colors'].astype('int64')
    df['price'] = df['price'].astype(float) * toRP

def bersihkan_data(df):
    df.dropna(subset=['rating'], inplace=True)
    df.dropna(subset=['colors'], inplace=True)
    df.dropna(subset=['price'], inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

def transform_dataset(raw_products):
    """Membersihkan dan mengubah data ke dalam bentuk DataFrame yang terstruktur."""
    if not raw_products:
        return pd.DataFrame(columns=['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp'])
    
    df = pd.DataFrame(raw_products)

    if df.empty or 'price' not in df.columns:
        return df

    # Filter baris dengan judul tidak valid seperti "unknown"
    if 'title' in df.columns:
        # Hapus baris dengan judul yang mengandung 'unknown' (case insensitive)
        df = df[~df['title'].str.lower().str.contains('unknown', na=False)]
    
    # Bersihkan kolom prize
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)

    # Bersihkan kolom rating
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)

    # Bersihkan kolom colors
    df['colors'] = df['colors'].replace(r'[^0-9]', '', regex=True).replace('', np.nan)

    # Bersihkan kolom size
    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)

    # Bersihkan kolom gender
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    # Bersihkan kolom rating untuk memastikan hanya dua angka desimal
    df['rating'] = df['rating'].apply(lambda x: float(str(x)[:str(x).find('.')+2]) if '.' in str(x) else float(x))

    # Ubah tipe data kolom
    ubah_tipedata(df)

    # Bersihkan data dari nilai yang tidak valid
    bersihkan_data(df)

    # Tambahkan kolom timestamp
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #ubah tipe data timestamp menjadi datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Set timezone ke Asia/Jakarta
    df['timestamp'] = df['timestamp'].dt.tz_localize('Asia/Jakarta')

    return df
