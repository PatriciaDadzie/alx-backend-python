
# Python Generators Project - Seeding MySQL Database

This project sets up and seeds a MySQL database **ALX_prodev** with user data from `user_data.csv`.

---

## Features
- Creates database `ALX_prodev` if it does not exist.
- Creates table `user_data` with the following schema:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Inserts sample data from `user_data.csv`.

---

## Functions in `seed.py`
- `connect_db()` → Connect to MySQL server.
- `create_database(connection)` → Create `ALX_prodev` database if missing.
- `connect_to_prodev()` → Connect directly to `ALX_prodev`.
- `create_table(connection)` → Create `user_data` table if not exists.
- `insert_data(connection, data)` → Insert rows from CSV into `user_data`.

---

## Usage
1. Start MySQL server and ensure credentials are correct in `seed.py`.
2. Run the provided `0-main.py`:

```bash
./0-main.py
