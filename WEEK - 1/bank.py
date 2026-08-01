from account import Account
from exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError
)


accounts = {}
next_account_id = 1


def create_account(customer_name):
    global next_account_id

    if not customer_name.strip():
        raise ValueError("Customer name cannot be empty.")

    account = Account(
        id=next_account_id,
        customer_name=customer_name,
        balance=0.0
    )

    accounts[next_account_id] = account

    next_account_id += 1

    return account


def get_account(account_id):
    if account_id not in accounts:
        raise AccountNotFoundError("Account not found.")

    return accounts[account_id]


def deposit(account_id, amount):
    if amount <= 0:
        raise InvalidAmountError("Deposit amount must be greater than zero.")

    account = get_account(account_id)

    account.balance += amount

    return account.balance


def withdraw(account_id, amount):
    if amount <= 0:
        raise InvalidAmountError("Withdrawal amount must be greater than zero.")

    account = get_account(account_id)

    if amount > account.balance:
        raise InsufficientFundsError("Insufficient balance.")

    account.balance -= amount

    return account.balance


def check_balance(account_id):
    account = get_account(account_id)

    return account.balance


def close_account(account_id):
    account = get_account(account_id)

    del accounts[account_id]

    return account