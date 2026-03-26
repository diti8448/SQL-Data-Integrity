# SQL Data Integrity & Unit Testing (HrvatskaDB)

This project demonstrates integration between Python and SQL Server with a focus on **data integrity validation and automated testing**.

## Key Features
- Automated testing using Python (`unittest`)
- Validation of relational integrity (JOINs, foreign keys)
- Unicode support for Croatian characters
- Separation of database layer and test logic

## Tech Stack
- Python
- SQL Server
- pyodbc
- unittest

## Use Case
Simulates real-world database validation scenarios where data consistency and integrity must be ensured (e.g. enterprise systems, backend services).

## What I Learned
- Writing unit tests for database-driven applications
- Validating relational data using SQL JOIN operations
- Integrating Python with SQL Server using pyodbc
- Ensuring data integrity through automated checks

## How to Run
1. Install dependencies:
   pip install -r requirements.txt
2. Execute SQL script in SQL Server
3. Run tests:
   python test_database.py