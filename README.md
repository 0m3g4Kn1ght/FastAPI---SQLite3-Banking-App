# Simple Banking API using FastAPI & SQLite3

This is a lightweight banking API built with **FastAPI** and **SQLite3**. It allows users to:

- Create accounts
- Deposit and withdraw money
- Transfer funds between accounts
- Check account balance

---

## Features

- Create user accounts
- Deposit and withdraw funds
- Transfer money between accounts
- Check current balance
- SQLite3 database (no external dependencies)

---

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

---

## Project Structure

```
.
├── main.py         # FastAPI application
├── db.py          # SQLite3 Database
└── bank.db
```

---

## ▶Running the App

Start the server using:

```bash
python -m uvicorn main:app --reload
```

This will start the server at:

```
http://127.0.0.1:8000
```

Explore the API docs at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

| Method | Endpoint          | Description                     |
|--------|-------------------|---------------------------------|
| POST   | `/create`         | Create a new account            |
| GET    | `/balance/{id}`   | Check account balance           |
| POST   | `/deposit`        | Deposit money into an account   |
| POST   | `/withdraw`       | Withdraw money from an account  |
| POST   | `/transfer`       | Transfer money between accounts |

---

## Example JSON Requests

### Create Account
```json
POST /create
{
  "name": "Ashwin"
}
```

### Deposit
```json
POST /deposit
{
  "account_id": 1,
  "amount": 60000
}
```

### Withdraw
```json
POST /withdraw
{
  "account_id": 1,
  "amount": 200
}
```

### Transfer
```json
POST /transfer
{
  "from_id": 1,
  "to_id": 2,
  "amount": 100
}
```

---

## License

Apache-2.0 License — use freely for learning, testing, or extending!
