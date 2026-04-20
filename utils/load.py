import pandas as pd
from sqlalchemy import create_engine

def save_to_csv(dataframe):
    """Menyimpan DataFrame ke file CSV lokal."""
    dataframe.to_csv("products.csv", index=False)
    print("Data berhasil disimpan ke file CSV")

def save_to_postgresql(dataframe):
    """Menyimpan DataFrame ke dalam tabel PostgreSQL."""
    try:
        # Buat koneksi ke PostgreSQL menggunakan SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://satss:121@localhost:5432/product_db')

        # Simpan DataFrame ke dalam tabel PostgreSQL (replace = timpa jika tabel sudah ada)
        dataframe.to_sql('products', engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL")

    except Exception as error:
        print(f"Gagal menyimpan data ke PostgreSQL: {error}")