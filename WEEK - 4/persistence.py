from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class AccountRecord:
    account_id: int
    customer_name: str
    balance: float = 0.0


@dataclass
class TransactionRecord:
    transaction_id: int
    transaction_type: str
    amount: float
    timestamp: datetime


def datetime_serializer(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()

    raise TypeError(
        f"Object of type {type(value).__name__} "
        "is not JSON serializable"
    )


def serialize_account(account: AccountRecord) -> dict[str, Any]:
    return asdict(account)


def serialize_transaction(
    transaction: TransactionRecord,
) -> dict[str, Any]:
    data = asdict(transaction)
    data["timestamp"] = transaction.timestamp.isoformat()
    return data


def save_json(
    path: Path,
    data: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            data,
            indent=4,
            default=datetime_serializer,
        ),
        encoding="utf-8",
    )


def load_json(
    path: Path,
) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def deserialize_account(
    data: dict[str, Any],
) -> AccountRecord:
    return AccountRecord(
        account_id=int(data["account_id"]),
        customer_name=str(data["customer_name"]),
        balance=float(data["balance"]),
    )


def deserialize_transaction(
    data: dict[str, Any],
) -> TransactionRecord:
    return TransactionRecord(
        transaction_id=int(data["transaction_id"]),
        transaction_type=str(data["transaction_type"]),
        amount=float(data["amount"]),
        timestamp=datetime.fromisoformat(
            data["timestamp"]
        ),
    )