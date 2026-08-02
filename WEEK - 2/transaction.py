from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_type: str
    amount: float
    related_account_id: int | None = None