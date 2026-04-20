import requests
from bs4 import BeautifulSoup
import time

# Jumlah halaman maksimum yang akan di-scrape
MAX_PAGE = 50

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_product_data(card):
    # Ambil informasi produk dari elemen HTML
    title = card.find('h3', class_='product-title')
    price = card.find('div', class_='price-container')
    rating = card.find('p', string=lambda t: t and 'Rating' in t)
    colors = card.find('p', string=lambda t: t and 'Colors' in t)
    size = card.find('p', string=lambda t: t and 'Size' in t)
    gender = card.find('p', string=lambda t: t and 'Gender' in t)

    # Susun data ke dalam dictionary
    product = {
        'title': title.text.strip() if title else 'Unknown Title',
        'price': price.text.strip() if price else 'Price Not Available',
        'rating': rating.text.strip() if rating else 'No Rating',
        'colors': colors.text.strip() if colors else 'No Color Info',
        'size': size.text.strip() if size else 'No Size Info',
        'gender': gender.text.strip() if gender else 'No Gender Info',
    }
    return product

def fetch_page_content(url):
    """"Mengambil konten HTML dari URL yang diberikan dengan penanganan kesalahan."""
    # Kirim permintaan HTTP ke halaman
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        raise Exception(f"Gagal mengakses {url}: {error}")


def scrape_website(url, delay = 1):
    """Mengambil data produk dari halaman koleksi berdasarkan URL."""
    data = []
    base_url = url
    response = fetch_page_content(base_url)
    print(f"Scraping halaman: {base_url}")

    try:
        # Parsing isi halaman dengan BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')
        # Temukan semua elemen kartu produk
        product_element = soup.find_all('div', class_='collection-card')
        # Cek apakah ada produk ditemukan atau tidak
        if not product_element:
            print(f"Tidak ada produk ditemukan di halaman {base_url}")
        for article in product_element:
            product = extract_product_data(article)
            data.append(product)
        print(f"{len(data)} produk berhasil diambil dari {base_url}")
    except Exception as parse_error:
        raise Exception(f"Terjadi kesalahan saat parsing HTML: {parse_error}")
    
    
    for page_number in range(2,MAX_PAGE + 1): 
        page_url = f"{url}page{page_number}"
        response = fetch_page_content(page_url)
        print(f"Scraping halaman ke-{page_number}: {page_url}")

        try:
            # Parsing isi halaman dengan BeautifulSoup
            soup = BeautifulSoup(response, 'html.parser')
            # Temukan semua elemen kartu produk
            product_element = soup.find_all('div', class_='collection-card')
            if not product_element:
                print(f"Tidak ada produk ditemukan di halaman {url}")
            for article in product_element:
                product = extract_product_data(article)
                data.append(product)
            print(f"{len(data)} produk berhasil diambil dari {url}")
            page_number += 1
            time.sleep(delay) # Delay sebelum halaman berikutnya

        except Exception as parse_error:
            raise Exception(f"Terjadi kesalahan saat parsing HTML: {parse_error}")

    return data
