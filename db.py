import sqlite3

DB_NAME = "bank.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL DEFAULT 0.0
            )
        """)
        conn.commit()

def create_account(name: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, 0.0))
        conn.commit()
        return cursor.lastrowid

def get_account(account_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM accounts WHERE id = ?", (account_id,))
        return cursor.fetchone()

def update_balance(account_id: int, amount: float):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        conn.commit()

def transfer_money(from_id: int, to_id: int, amount: float):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,))
        from_balance = cursor.fetchone()
        if not from_balance or from_balance[0] < amount:
            raise ValueError("Insufficient funds")
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
        conn.commit()
