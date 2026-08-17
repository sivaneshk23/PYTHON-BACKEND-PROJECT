from datetime import datetime
from pathlib import Path

from persistence import (
    AccountRecord,
    TransactionRecord,
    deserialize_account,
    deserialize_transaction,
    load_json,
    save_json,
    serialize_account,
    serialize_transaction,
)


def test_account_serialization_preserves_data():
    account = AccountRecord(
        account_id=1001,
        customer_name="Sivanesh",
        balance=5000.0,
    )

    data = serialize_account(account)

    restored = deserialize_account(data)

    assert restored == account


def test_transaction_serialization_preserves_datetime():
    transaction = TransactionRecord(
        transaction_id=1,
        transaction_type="deposit",
        amount=5000.0,
        timestamp=datetime(
            2026,
            8,
            17,
            10,
            30,
            15,
            123456,
        ),
    )

    data = serialize_transaction(transaction)

    restored = deserialize_transaction(data)

    assert restored == transaction


def test_json_round_trip_preserves_accounts(
    tmp_path: Path,
):
    accounts = [
        AccountRecord(
            account_id=1001,
            customer_name="Sivanesh",
            balance=5000.0,
        ),
        AccountRecord(
            account_id=1002,
            customer_name="Kumar",
            balance=2500.0,
        ),
    ]

    path = tmp_path / "accounts.json"

    data = [
        serialize_account(account)
        for account in accounts
    ]

    save_json(path, data)

    loaded_data = load_json(path)

    restored_accounts = [
        deserialize_account(item)
        for item in loaded_data
    ]

    assert restored_accounts == accounts


def test_json_round_trip_preserves_transactions(
    tmp_path: Path,
):
    transactions = [
        TransactionRecord(
            transaction_id=1,
            transaction_type="deposit",
            amount=5000.0,
            timestamp=datetime(
                2026,
                8,
                17,
                10,
                0,
            ),
        ),
        TransactionRecord(
            transaction_id=2,
            transaction_type="withdraw",
            amount=1000.0,
            timestamp=datetime(
                2026,
                8,
                17,
                11,
                0,
            ),
        ),
    ]

    path = tmp_path / "transactions.json"

    data = [
        serialize_transaction(transaction)
        for transaction in transactions
    ]

    save_json(path, data)

    loaded_data = load_json(path)

    restored_transactions = [
        deserialize_transaction(item)
        for item in loaded_data
    ]

    assert restored_transactions == transactions


def test_load_json_returns_empty_list_for_missing_file(
    tmp_path: Path,
):
    path = tmp_path / "missing.json"

    result = load_json(path)

    assert result == []