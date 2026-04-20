from utils.extract import scrape_website
from utils.transform import transform_dataset
from utils.load import save_to_csv, save_to_postgresql

def main():
    """Main function to run the ETL process: ETL - Extract, Transform, Load."""
    
    # URL dasar untuk scraping
    BASE_URL = 'https://fashion-studio.dicoding.dev/'

    # Ambil data dari URL
    products = scrape_website(BASE_URL)

    # Bersihkan dan transformasi data hasil scraping
    cleaned_data = transform_dataset(products)

    # Simpan data yang telah dibersihkan ke file CSV
    save_to_csv(cleaned_data)

    # Simpan data yang telah dibersihkan ke database PostgreSQL
    save_to_postgresql(cleaned_data)

    # Proses selesai
    print("Proses scraping dan penyimpanan data selesai.")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()
