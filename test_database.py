import pyodbc
import unittest
from datetime import datetime


class TestHrvatskaDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Inicijalizacija konekcije — pokreće se jednom za sve testove.
        Koristimo setUpClass umjesto setUp radi performansi
        (jedna konekcija umjesto N konekcija).
        """
        cls.server = r'DITI8448\VE_SERVER'
        cls.database = 'HrvatskaDB'
        cls.conn_str = (
            f'DRIVER={{SQL Server}};'
            f'SERVER={cls.server};'
            f'DATABASE={cls.database};'
            f'Trusted_Connection=yes;'
        )
        try:
            cls.conn = pyodbc.connect(cls.conn_str)
            cls.cursor = cls.conn.cursor()
            print(f"\n--- Testiranje započeto: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        except Exception as e:
            print(f"Konekcija nije uspjela: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Zatvaranje konekcije nakon svih testova."""
        if hasattr(cls, 'conn'):
            cls.conn.close()

    # ----------------------------------------------------------
    # TEST 1 — Unicode validacija
    # ----------------------------------------------------------
    def test_1_unicode_podaci(self):
        """Provjera ispravnosti Unicode znakova (Đ, š, č, ž)."""
        self.cursor.execute("SELECT Naziv FROM Znamenitost WHERE Naziv LIKE N'%Đ%'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "Greška: SQL nije pronašao znak 'Đ'. Provjeri N prefiks!")
        self.assertIn('Đ', result[0], f"Očekivan 'Đ', dobiveno: {result[0]}")

    # ----------------------------------------------------------
    # TEST 2 — Kvantiteta podataka
    # ----------------------------------------------------------
    def test_2_kvantiteta_podataka(self):
        """Provjera ima li dovoljno gradova u bazi (minimalno 7)."""
        self.cursor.execute("SELECT COUNT(*) FROM Grad")
        count = self.cursor.fetchone()[0]
        self.assertGreaterEqual(count, 7, f"Baza je previše prazna (samo {count} gradova).")

    # ----------------------------------------------------------
    # TEST 3 — Kompleksni JOIN kroz 3 tablice
    # ----------------------------------------------------------
    def test_3_kompleksni_join(self):
        """
        Provjera relacije kroz 3 tablice:
        Znamenitost → Grad → Županija
        Testira ispravnost FK veza i JOIN logike.
        """
        query = """
            SELECT z.Naziv, g.Naziv, zp.Naziv
            FROM Znamenitost z
            JOIN Grad g  ON z.GradId    = g.Id
            JOIN Zupanija zp ON g.ZupanijaId = zp.Id
            WHERE z.Naziv LIKE N'Arena%'
        """
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        self.assertIsNotNone(res, "Znamenitost 'Arena%' nije pronađena!")
        self.assertEqual(res[1], 'Pula',      f"Očekivan grad 'Pula', dobiven: {res[1]}")
        self.assertEqual(res[2], 'Istarska',  f"Očekivana županija 'Istarska', dobivena: {res[2]}")

    # ----------------------------------------------------------
    # TEST 4 — Matematička validacija godine
    # ----------------------------------------------------------
    def test_4_logika_godina(self):
        """Matematička provjera: nijedna znamenitost ne smije biti iz budućnosti."""
        trenutna = datetime.now().year
        self.cursor.execute("SELECT Naziv, GodinaIzgradnje FROM Znamenitost WHERE GodinaIzgradnje IS NOT NULL")
        for naziv, godina in self.cursor.fetchall():
            self.assertLessEqual(
                godina, trenutna,
                f"Znamenitost '{naziv}' ima nemoguću godinu: {godina}"
            )

    # ----------------------------------------------------------
    # TEST 5 — CHECK constraint (negativno stanovništvo)
    # ----------------------------------------------------------
    def test_5_stanovnistvo_pozitivno(self):
        """
        Provjera CHECK constrainta:
        Baza mora odbiti unos negativnog stanovništva.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Grad (Naziv, Stanovnistvo, ZupanijaId) VALUES (N'TestGrad', -1, 1)"
            )
            self.conn.commit()
            # Ako INSERT prođe bez greške — test pada
            self.cursor.execute("DELETE FROM Grad WHERE Naziv = N'TestGrad'")
            self.conn.commit()
            self.fail("Baza je dopustila negativno stanovništvo — CHECK constraint ne radi!")
        except pyodbc.IntegrityError:
            self.conn.rollback()  # Očekivano — baza je odbila grešku

    # ----------------------------------------------------------
    # TEST 6 — UNIQUE constraint (duplikati županija)
    # ----------------------------------------------------------
    def test_6_zupanija_unikatna(self):
        """
        Provjera UNIQUE constrainta:
        Baza mora odbiti duplikate naziva županija.
        """
        naziv = 'Krapinsko-zagorska'
        try:
            self.cursor.execute("INSERT INTO Zupanija (Naziv) VALUES (?)", (naziv,))
            self.conn.commit()
            self.fail("Baza je dopustila dupli unos naziva županije!")
        except pyodbc.IntegrityError:
            self.conn.rollback()  # Očekivano — UNIQUE constraint je odbio duplikat

    # ----------------------------------------------------------
    # TEST 7 — FOREIGN KEY constraint
    # ----------------------------------------------------------
    def test_7_foreign_key_constraint(self):
        """
        Provjera FK constrainta:
        Grad ne smije biti unesen s nepostojećim ZupanijaId.
        """
        try:
            self.cursor.execute(
                "INSERT INTO Grad (Naziv, Stanovnistvo, ZupanijaId) VALUES (N'TestGrad', 1000, 9999)"
            )
            self.conn.commit()
            self.cursor.execute("DELETE FROM Grad WHERE Naziv = N'TestGrad'")
            self.conn.commit()
            self.fail("Baza je dopustila unos grada s nepostojećim ZupanijaId!")
        except pyodbc.IntegrityError:
            self.conn.rollback()  # Očekivano — FK constraint je odbio unos

            # ----------------------------------------------------------
    # ----------------------------------------------------------
    # TEST 8 — Referencijalni integritet (Brisanje roditelja)
    # ----------------------------------------------------------
    def test_8_brisanje_zupanije_s_gradovima(self):
        """
        Provjera Foreign Key zaštite:
        Ne smije se moći obrisati županija koja ima povezane gradove.
        """
        # Id 1 je Krapinsko-zagorska, koja ima gradove u podacima
        # Id 1 je Krapinsko-zagorska
        zupanija_id = 1 
        try:
            self.cursor.execute("DELETE FROM Zupanija WHERE Id = ?", (zupanija_id,))
            self.conn.commit()
            self.fail("Baza je dopustila brisanje županije koja ima gradove! FK ne radi.")
        except pyodbc.IntegrityError:
            self.conn.rollback()  # Očekivano: SQL blokira brisanje zbog FK constrainta


if __name__ == '__main__':
    unittest.main(verbosity=2)
