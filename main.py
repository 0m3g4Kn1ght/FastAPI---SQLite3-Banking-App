from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import (
    init_db, create_account, get_account, get_all_accounts, search_accounts_by_name,
    update_balance, transfer_money, delete_account, get_total_balance, get_transactions
)

app = FastAPI(title="Advanced Banking App")

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
    return {"message": f"Account '{account.name}' created with ID {account_id}", "account_id": account_id}

@app.get("/accounts/")
def list_accounts():
    return {"accounts": get_all_accounts()}

@app.get("/accounts/search/{name}")
def search_accounts(name: str):
    return {"accounts": search_accounts_by_name(name)}

@app.get("/balance/{account_id}")
def check_balance(account_id: int):
    acc = get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": acc[0], "name": acc[1], "balance": acc[2]}

@app.post("/deposit/")
def deposit_money(txn: Transaction):
    acc = get_account(txn.account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    if txn.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    update_balance(txn.account_id, txn.amount)
    return {"message": f"Deposit of {txn.amount} to account '{acc[1]}' successful"}

@app.post("/withdraw/")
def withdraw_money(txn: Transaction):
    acc = get_account(txn.account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    if txn.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if acc[2] < txn.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    update_balance(txn.account_id, -txn.amount)
    return {"message": f"Withdrawal of {txn.amount} from account '{acc[1]}' successful"}

@app.post("/transfer/")
def transfer_funds(data: Transfer):
    from_acc = get_account(data.from_id)
    to_acc = get_account(data.to_id)
    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if data.amount > from_acc[2]:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    try:
        transfer_money(data.from_id, data.to_id, data.amount)
        return {"message": f"Transfer of {data.amount} from '{from_acc[1]}' to '{to_acc[1]}' successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete_account/{account_id}")
def remove_account(account_id: int):
    acc = get_account(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    delete_account(account_id)
    return {"message": f"Account '{acc[1]}' deleted successfully"}

@app.get("/bank_total/")
def bank_total():
    return {"total_balance": get_total_balance()}

@app.get("/transactions/{account_id}")
def account_transactions(account_id: int):
    if not get_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    return {"transactions": get_transactions(account_id)}
