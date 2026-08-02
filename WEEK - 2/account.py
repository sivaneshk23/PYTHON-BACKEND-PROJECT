from dataclasses import dataclass


@dataclass
class Account:
    id: int
    customer_name: str
    balance: float = 0.0