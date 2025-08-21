from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_account():
    response = client.post("/create_account/", json={"name": "Test User"})
    assert response.status_code == 200
    data = response.json()
    assert "account_id" in data
    assert data["message"] == f"Account 'Test User' created with ID {data['account_id']}"


def test_initial_balance_not_found():
    response = client.get("/balance/9999")
    assert response.status_code == 404
    assert "Account not found" in response.json()["detail"]


def test_deposit_successful():
    account = client.post("/create_account/", json={"name": "Deposit User"}).json()
    account_id = account["account_id"]

    response = client.post("/deposit/", json={"account_id": account_id, "amount": 500.0})
    assert response.status_code == 200
    assert f"Deposit of 500.0 to account 'Deposit User' successful" in response.json()["message"]


def test_deposit_negative_amount():
    account = client.post("/create_account/", json={"name": "Negative User"}).json()
    account_id = account["account_id"]

    response = client.post("/deposit/", json={"account_id": account_id, "amount": -100.0})
    assert response.status_code == 400
    assert "Amount must be positive" in response.json()["detail"]


def test_withdraw_successful():
    account = client.post("/create_account/", json={"name": "Withdraw User"}).json()
    account_id = account["account_id"]
    client.post("/deposit/", json={"account_id": account_id, "amount": 1000.0})

    response = client.post("/withdraw/", json={"account_id": account_id, "amount": 200.0})
    assert response.status_code == 200
    assert f"Withdrawal of 200.0 from account 'Withdraw User' successful" in response.json()["message"]


def test_withdraw_insufficient_funds():
    account = client.post("/create_account/", json={"name": "Poor User"}).json()
    account_id = account["account_id"]

    response = client.post("/withdraw/", json={"account_id": account_id, "amount": 200.0})
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]


def test_transfer_successful():
    acc1 = client.post("/create_account/", json={"name": "Sender"}).json()
    acc2 = client.post("/create_account/", json={"name": "Receiver"}).json()

    client.post("/deposit/", json={"account_id": acc1["account_id"], "amount": 2000.0})

    response = client.post("/transfer/", json={
        "from_id": acc1["account_id"],
        "to_id": acc2["account_id"],
        "amount": 1000.0
    })
    assert response.status_code == 200
    assert f"Transfer of 1000.0 from 'Sender' to 'Receiver' successful" in response.json()["message"]


def test_transfer_insufficient_funds():
    acc1 = client.post("/create_account/", json={"name": "Low Sender"}).json()
    acc2 = client.post("/create_account/", json={"name": "Low Receiver"}).json()

    response = client.post("/transfer/", json={
        "from_id": acc1["account_id"],
        "to_id": acc2["account_id"],
        "amount": 1000.0
    })
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]


def test_transfer_non_existent_account():
    acc1 = client.post("/create_account/", json={"name": "Valid Sender"}).json()

    response = client.post("/transfer/", json={
        "from_id": acc1["account_id"],
        "to_id": 9999,
        "amount": 500.0
    })
    assert response.status_code == 404
    assert "Account not found" in response.json()["detail"]
