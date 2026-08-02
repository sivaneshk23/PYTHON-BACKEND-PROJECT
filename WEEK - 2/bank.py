from collections import defaultdict

from account import Account
from transaction import Transaction


class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = defaultdict(list)
        self.customer_index = defaultdict(list)
        self.next_account_id = 1

    def create_account(self, customer_name, initial_balance):
        if initial_balance <= 0:
            raise InvalidAmountError("Initial balance must be greater than 0.")

        account_id = self.next_account_id
        self.next_account_id += 1

        account = Account(
            id=account_id,
            customer_name=customer_name,
            balance=initial_balance
        )

        self.accounts[account_id] = account
        self.customer_index[customer_name.lower()].append(account_id)

        return account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError("Account not found.")

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than 0.")

        account = self.get_account(account_id)

        account.balance += amount

        self.transactions[account_id].append(
            Transaction("deposit", amount)
        )

    def withdraw(self, account_id, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than 0.")

        account = self.get_account(account_id)

        if amount > account.balance:
            raise InsufficientFundsError("Insufficient balance.")

        account.balance -= amount

        self.transactions[account_id].append(
            Transaction("withdraw", amount)
        )

    def get_balance(self, account_id):
        account = self.get_account(account_id)
        return account.balance

    def transfer(self, from_id, to_id, amount):
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be greater than 0.")

        # Validate BOTH accounts before changing any balance.
        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)

        if amount > from_account.balance:
            raise InsufficientFundsError("Insufficient balance.")

        old_from_balance = from_account.balance
        old_to_balance = to_account.balance

        try:
            from_account.balance -= amount
            to_account.balance += amount

            self.transactions[from_id].append(
                Transaction("transfer_out", amount, to_id)
            )

            self.transactions[to_id].append(
                Transaction("transfer_in", amount, from_id)
            )

        except Exception:
            # Manual rollback
            from_account.balance = old_from_balance
            to_account.balance = old_to_balance
            raise

    def reverse_last_transaction(self, account_id):
        account = self.get_account(account_id)

        if not self.transactions[account_id]:
            raise ValueError("No transaction available to reverse.")

        transaction = self.transactions[account_id][-1]

        if transaction.transaction_type == "deposit":
            if transaction.amount > account.balance:
                raise InsufficientFundsError(
                    "Cannot reverse deposit because the money is no longer available."
                )

            account.balance -= transaction.amount

        elif transaction.transaction_type == "withdraw":
            account.balance += transaction.amount

        else:
            raise ValueError(
                "Transfer reversal must be handled from the sender account."
            )

        self.transactions[account_id].pop()

    def find_accounts_by_customer(self, customer_name):
        account_ids = self.customer_index.get(
            customer_name.lower(),
            []
        )

        return [
            self.accounts[account_id]
            for account_id in account_ids
            if account_id in self.accounts
        ]