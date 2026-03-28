# SQL Data Integrity & Unit Testing (HrvatskaDB)

This project demonstrates integration between **Python and SQL Server** with a focus on **data integrity validation and automated testing**.

## Key Features

- Automated testing using Python `unittest`
- Validation of SQL constraints: `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`
- Relational integrity testing with multi-table `JOIN` operations
- Unicode support for Croatian characters (`Đ`, `š`, `č`, `ž`)
- Clean separation: schema file vs. data file

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Test logic |
| SQL Server | Relational database |
| pyodbc | Python ↔ SQL Server connection |
| unittest | Automated testing framework |

## Project Structure

```
SQL-Data-Integrity/
├── HrvatskaDB_schema.sql   ← CREATE TABLE (run first)
├── HrvatskaDB_data.sql     ← INSERT data (run second)
├── test_database.py        ← 8 automated tests
├── requirements.txt
└── README.md
```

## What the Tests Cover

| Test | What it validates |
|---|---|
| `test_1_unicode_podaci` | Croatian characters (Đ) stored correctly |
| `test_2_kvantiteta_podataka` | Minimum data quantity check |
| `test_3_kompleksni_join` | 3-table JOIN relational logic |
| `test_4_logika_godina` | No future build years (math validation) |
| `test_5_stanovnistvo_pozitivno` | CHECK constraint rejects negative population |
| `test_6_zupanija_unikatna` | UNIQUE constraint rejects duplicate county names |
| `test_7_foreign_key_constraint` | FK constraint rejects invalid ZupanijaId |
  `test_8_brisanje_zupanije_s_gradovima` | FK protection against deleting a parent with children |

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up the database

Open SQL Server Management Studio and run the scripts **in order**:

```
1. HrvatskaDB_schema.sql   ← creates database and tables
2. HrvatskaDB_data.sql     ← inserts test data
```

### 3. Configure your server name

In `test_database.py`, update line 16 with your SQL Server instance name:

```python
cls.server = r'YOUR_SERVER\INSTANCE_NAME'
```

### 4. Run tests

```bash
python test_database.py
```

Expected output:
```
--- Testiranje započeto: 2026-01-01 12:00:00 ---

test_1_unicode_podaci ... ok
test_2_kvantiteta_podataka ... ok
test_3_kompleksni_join ... ok
test_4_logika_godina ... ok
test_5_stanovnistvo_pozitivno ... ok
test_6_zupanija_unikatna ... ok
test_7_foreign_key_constraint ... ok
test_8_brisanje_zupanije_s_gradovima ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.350s

OK

## What I Learned

- Writing unit tests for database-driven applications
- Validating SQL constraints (`CHECK`, `UNIQUE`, `FOREIGN KEY`) through Python
- Using `rollback()` to safely test constraint violations without corrupting data
- Multi-table `JOIN` validation across relational schema
- Integrating Python with SQL Server using `pyodbc`
- Difference between `setUpClass` and `setUp` (performance: one connection vs. N connections)
- Unicode handling with `N''` prefix in SQL Server

## Author

Sandi Ćamilov — Python Developer
