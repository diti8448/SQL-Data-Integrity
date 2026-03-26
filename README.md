# SQL Data Integrity & Unit Testing (HrvatskaDB)

Ovaj projekt demonstrira napredno povezivanje Pythona s SQL Serverom uz primjenu **Unit Testing** metodologije za validaciju relacijskih podataka.

## Ključne funkcionalnosti
* **Automatsko testiranje**: Provjera poslovne logike kroz `unittest` framework.
* **Relacijski integritet**: Validacija `JOIN` operacija i stranih ključeva.
* **Unicode podrška**: Ispravan rad s hrvatskim znakovima (N prefiks u SQL-u).
* **Čist kod**: Odvajanje baze (SQL) od testne logike (Python).

## Kako pokrenuti?
1. Instalirajte ovisnosti: `pip install -r requirements.txt`
2. Izvršite SQL skriptu u SSMS-u.
3. Pokrenite testove: `python test_database.py`