import unittest
from unittest.mock import patch, MagicMock, ANY
import pandas as pd
from utils.load import save_to_csv, save_to_postgresql

csv_dummy = "dummy.csv"

class TestLoad(unittest.TestCase):
    """Pengujian terhadap fungsi penyimpanan data (CSV dan PostgreSQL)."""

    def test_simpan_ke_csv(self):
        """Mengujikan fungsi penyimpanan DataFrame ke file CSV."""
        dummy_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            save_to_csv(dummy_df)
            mock_to_csv.assert_called_once_with(ANY, index=False)

    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql_sukses(self, mock_create_engine):
        """Mengujikan penyimpanan data ke PostgreSQL ketika koneksi berhasil."""
        dummy_df = pd.DataFrame({'col1': [1], 'col2': [2]})
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        with patch.object(dummy_df, 'to_sql') as mock_to_sql, patch('builtins.print') as mock_print:
            save_to_postgresql(dummy_df)

            # Pastikan koneksi dibuat dengan parameter yang benar
            mock_create_engine.assert_called_once_with(
                'postgresql+psycopg2://satss:121@localhost:5432/product_db'
            )

            # Pastikan pemanggilan penyimpanan ke tabel benar
            mock_to_sql.assert_called_once_with('products', mock_engine, if_exists='replace', index=False)

            # Verifikasi pesan keberhasilan ditampilkan
            mock_print.assert_any_call("Data berhasil disimpan ke PostgreSQL")

    @patch('utils.load.create_engine')
    def test_simpan_ke_postgresql_gagal(self, mock_create_engine):
        """Mengujikan kasus ketika penyimpanan ke PostgreSQL gagal akibat error koneksi."""
        dummy_df = pd.DataFrame({'col1': [1]})
        mock_create_engine.side_effect = Exception("Koneksi gagal")

        with patch('builtins.print') as mock_print:
            save_to_postgresql(dummy_df)

            # Pastikan error ditangani dan pesan kesalahan dicetak
            semua_pesan = [call_args[0][0] for call_args in mock_print.call_args_list]
            self.assertTrue(any("Gagal menyimpan data ke PostgreSQL" in msg for msg in semua_pesan))

if __name__ == '__main__':
    unittest.main()
