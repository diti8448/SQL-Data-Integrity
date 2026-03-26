import pyodbc
import unittest
from datetime import datetime

class TestHrvatskaDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = r'DITI8448\VE_SERVER' 
        cls.database = 'HrvatskaDB'
        cls.conn_str = f'DRIVER={{SQL Server}};SERVER={cls.server};DATABASE={cls.database};Trusted_Connection=yes;'
        try:
            cls.conn = pyodbc.connect(cls.conn_str)
            cls.cursor = cls.conn.cursor()
        except Exception as e:
            print(f"Konekcija nije uspjela: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'conn'):
            cls.conn.close()

    def test_1_unicode_podaci(self):
        """Provjera ispravnosti Unicode znakova (Đ, š, č)"""
        # Tražimo Đalskog pomoću Unicode upita
        self.cursor.execute("SELECT Naziv FROM Znamenitost WHERE Naziv LIKE N'%Đ%'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Greška: SQL nije pronašao znak 'Đ'. Provjeri N prefiks!")
        self.assertIn('Đ', result[0], f"Očekivan 'Đ', dobiveno: {result[0]}")

    def test_2_kvantiteta_podataka(self):
        """Provjera ima li dovoljno gradova u bazi (Problem 2)"""
        self.cursor.execute("SELECT COUNT(*) FROM Grad")
        count = self.cursor.fetchone()[0]
        self.assertGreaterEqual(count, 7, f"Baza je previše prazna (samo {count} gradova).")

    def test_3_kompleksni_join(self):
        """Provjera relacije: Povezuje li sustav ispravno Arenu, Pulu i Istru?"""
        query = """
            SELECT z.Naziv, g.Naziv, zp.Naziv
            FROM Znamenitost z
            JOIN Grad g ON z.GradId = g.Id
            JOIN Zupanija zp ON g.ZupanijaId = zp.Id
            WHERE z.Naziv LIKE N'Arena%'
        """
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        self.assertEqual(res[1], 'Pula')
        self.assertEqual(res[2], 'Istarska')

    def test_4_logika_godina(self):
        """Matematička provjera: Nijedna znamenitost nije iz budućnosti"""
        trenutna = datetime.now().year
        self.cursor.execute("SELECT Naziv, GodinaIzgradnje FROM Znamenitost")
        for naziv, godina in self.cursor.fetchall():
            self.assertLessEqual(godina, trenutna, f"{naziv} ima nemoguću godinu: {godina}")

if __name__ == '__main__':
    unittest.main()