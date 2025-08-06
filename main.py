from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import init_db, create_account, get_account, update_balance, transfer_money

app = FastAPI(title="Simple Banking App")

init_db()

class AccountCreate(BaseModel):
    name: str

class Transaction(BaseModel):
    account_id: int
    amount: float

class Transfer(BaseModel):
    from_id: int
    to_id: int
    amount: float

@app.post("/create_account/")
def create_new_account(account: AccountCreate):
    account_id = create_account(account.name)
    return {"message": "Account created", "account_id": account_id}

@app.get("/balance/{account_id}")
def check_balance(account_id: int):
    acc = get_account(account_id)
    if acc:
        return {"account_id": acc[0], "name": acc[1], "balance": acc[2]}
    raise HTTPException(status_code=404, detail="Account not found")

@app.post("/deposit/")
def deposit_money(txn: Transaction):
    if txn.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if not get_account(txn.account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    update_balance(txn.account_id, txn.amount)
    return {"message": "Deposit successful"}

@app.post("/withdraw/")
def withdraw_money(txn: Transaction):
    acc = get_account(txn.account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    if txn.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if acc[2] < txn.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    update_balance(txn.account_id, -txn.amount)
    return {"message": "Withdrawal successful"}

@app.post("/transfer/")
def transfer_funds(data: Transfer):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if not get_account(data.from_id) or not get_account(data.to_id):
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        transfer_money(data.from_id, data.to_id, data.amount)
        return {"message": "Transfer successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
