import unittest
import pandas as pd
from utils.transform import transform_dataset

data_input = [
    {
        'title': 'Baju Keren',
        'price': '100.00',
        'rating': 'Rating: 4.5',
        'colors': 'Colors: 3',
        'size': 'Size: L',
        'gender': 'Gender: Male'
    },
    {
        'title': 'Unknown Title',
        'price': '50.00',
        'rating': 'Rating: 3.5',
        'colors': 'Colors: 2',
        'size': 'Size: M',
        'gender': 'Gender: Female'
    }
]

class TestTransform(unittest.TestCase):
    """Pengujian untuk fungsi pembersihan dan transformasi data produk."""
    def test_data_dengan_nilai_normal(self):
        """Mengujikan transformasi data yang valid dan lengkap."""

        hasil_df = transform_dataset(data_input)

        # Pastikan output berupa DataFrame
        self.assertIsInstance(hasil_df, pd.DataFrame)

        # Pastikan baris dengan judul tidak valid difilter
        self.assertNotIn('Unknown Title', hasil_df['title'].values)

        # Pastikan kolom timestamp ditambahkan
        self.assertIn('timestamp', hasil_df.columns)

        # Hanya satu baris valid yang tersisa
        self.assertEqual(len(hasil_df), 1)

    def test_data_kosong(self):
        """Mengujikan transformasi jika input berupa list kosong."""
        hasil_df = transform_dataset([])

        # Output tetap berupa DataFrame meskipun kosong
        self.assertIsInstance(hasil_df, pd.DataFrame)

        # Jumlah baris harus nol
        self.assertEqual(hasil_df.shape[0], 0)

        # Pastikan kolom sesuai dengan format yang diharapkan
        self.assertListEqual(
            list(hasil_df.columns),
            ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        )

if __name__ == '__main__':
    unittest.main()
