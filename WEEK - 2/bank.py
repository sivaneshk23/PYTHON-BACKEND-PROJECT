from collections import defaultdict

from account import Account
from transaction import Transaction
from storage_manager import load_data, save_data


class AccountNotFoundError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class Bank:
    def __init__(self, persistent=False):
        self.accounts = {}
        self.transactions = defaultdict(list)
        self.customer_index = defaultdict(list)

        self.next_account_id = 1
        self.next_transaction_id = 1

        self.persistent = persistent

        if self.persistent:
            self.load_state()

    def _create_transaction(
        self,
        transaction_type,
        amount,
        related_account_id=None
    ):
        transaction = Transaction(
            transaction_id=self.next_transaction_id,
            transaction_type=transaction_type,
            amount=amount,
            related_account_id=related_account_id
        )

        self.next_transaction_id += 1

        return transaction

    def create_account(self, customer_name, initial_balance):
        if initial_balance <= 0:
            raise InvalidAmountError(
                "Initial balance must be greater than 0."
            )

        account_id = self.next_account_id
        self.next_account_id += 1

        account = Account(
            id=account_id,
            customer_name=customer_name,
            balance=initial_balance
        )

        self.accounts[account_id] = account

        self.customer_index[
            customer_name.lower()
        ].append(account_id)

        self.save_state()

        return account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(
                "Account not found."
            )

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        if amount <= 0:
            raise InvalidAmountError(
                "Deposit amount must be greater than 0."
            )

        account = self.get_account(account_id)

        account.balance += amount

        transaction = self._create_transaction(
            "deposit",
            amount
        )

        self.transactions[account_id].append(
            transaction
        )

        self.save_state()

    def withdraw(self, account_id, amount):
        if amount <= 0:
            raise InvalidAmountError(
                "Withdrawal amount must be greater than 0."
            )

        account = self.get_account(account_id)

        if amount > account.balance:
            raise InsufficientFundsError(
                "Insufficient balance."
            )

        account.balance -= amount

        transaction = self._create_transaction(
            "withdraw",
            amount
        )

        self.transactions[account_id].append(
            transaction
        )

        self.save_state()

    def get_balance(self, account_id):
        account = self.get_account(account_id)
        return account.balance

    def transfer(self, from_id, to_id, amount):
        if amount <= 0:
            raise InvalidAmountError(
                "Transfer amount must be greater than 0."
            )

        if from_id == to_id:
            raise ValueError(
                "Sender and receiver accounts cannot be the same."
            )

        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)

        if amount > from_account.balance:
            raise InsufficientFundsError(
                "Insufficient balance."
            )

        old_from_balance = from_account.balance
        old_to_balance = to_account.balance

        try:
            from_account.balance -= amount
            to_account.balance += amount

            transfer_out = self._create_transaction(
                "transfer_out",
                amount,
                to_id
            )

            transfer_in = self._create_transaction(
                "transfer_in",
                amount,
                from_id
            )

            self.transactions[from_id].append(
                transfer_out
            )

            self.transactions[to_id].append(
                transfer_in
            )

            self.save_state()

        except Exception:
            from_account.balance = old_from_balance
            to_account.balance = old_to_balance
            raise

    def reverse_last_transaction(self, account_id):
        account = self.get_account(account_id)

        transactions = self.transactions[account_id]

        original_transaction = None

        for transaction in reversed(transactions):
            if (
                not transaction.reversed
                and transaction.transaction_type
                in {
                    "deposit",
                    "withdraw",
                    "transfer_out"
                }
            ):
                original_transaction = transaction
                break

        if original_transaction is None:
            raise ValueError(
                "No transaction available to reverse."
            )

        if original_transaction.transaction_type == "deposit":

            if original_transaction.amount > account.balance:
                raise InsufficientFundsError(
                    "Cannot reverse deposit because "
                    "the money is no longer available."
                )

            account.balance -= original_transaction.amount

            reversal = self._create_transaction(
                "deposit_reversal",
                original_transaction.amount
            )

            transactions.append(reversal)

            original_transaction.reversed = True

        elif original_transaction.transaction_type == "withdraw":

            account.balance += original_transaction.amount

            reversal = self._create_transaction(
                "withdraw_reversal",
                original_transaction.amount
            )

            transactions.append(reversal)

            original_transaction.reversed = True

        elif original_transaction.transaction_type == "transfer_out":

            receiver_id = (
                original_transaction.related_account_id
            )

            receiver = self.get_account(
                receiver_id
            )

            if original_transaction.amount > receiver.balance:
                raise InsufficientFundsError(
                    "Cannot reverse transfer because "
                    "the receiver has insufficient balance."
                )

            old_sender_balance = account.balance
            old_receiver_balance = receiver.balance

            try:
                receiver.balance -= original_transaction.amount
                account.balance += original_transaction.amount

                sender_reversal = self._create_transaction(
                    "transfer_reversal_in",
                    original_transaction.amount,
                    receiver_id
                )

                receiver_reversal = self._create_transaction(
                    "transfer_reversal_out",
                    original_transaction.amount,
                    account_id
                )

                transactions.append(
                    sender_reversal
                )

                self.transactions[
                    receiver_id
                ].append(
                    receiver_reversal
                )

                original_transaction.reversed = True

                for transaction in reversed(
                    self.transactions[receiver_id]
                ):
                    if (
                        transaction.transaction_type
                        == "transfer_in"
                        and transaction.related_account_id
                        == account_id
                        and transaction.amount
                        == original_transaction.amount
                        and not transaction.reversed
                    ):
                        transaction.reversed = True
                        break

            except Exception:
                account.balance = old_sender_balance
                receiver.balance = old_receiver_balance
                raise

        self.save_state()

    def find_accounts_by_customer(
        self,
        customer_name
    ):
        account_ids = self.customer_index.get(
            customer_name.lower(),
            []
        )

        return [
            self.accounts[account_id]
            for account_id in account_ids
            if account_id in self.accounts
        ]

    def get_transaction_history(self, account_id):
        self.get_account(account_id)

        return self.transactions[account_id]

    def save_state(self):
        if not self.persistent:
            return

        accounts = []

        for account in self.accounts.values():
            accounts.append({
                "id": account.id,
                "customer_name": account.customer_name,
                "balance": account.balance
            })

        transactions = []

        for account_id, account_transactions in (
            self.transactions.items()
        ):
            for transaction in account_transactions:
                transactions.append({
                    "account_id": account_id,
                    "transaction_id": transaction.transaction_id,
                    "transaction_type": transaction.transaction_type,
                    "amount": transaction.amount,
                    "related_account_id":
                        transaction.related_account_id,
                    "reversed": transaction.reversed
                })

        data = {
            "next_account_id": self.next_account_id,
            "next_transaction_id": self.next_transaction_id,
            "accounts": accounts,
            "transactions": transactions
        }

        save_data(data)

    def load_state(self):
        data = load_data()

        self.next_account_id = data.get(
            "next_account_id",
            1
        )

        self.next_transaction_id = data.get(
            "next_transaction_id",
            1
        )

        self.accounts.clear()
        self.transactions.clear()
        self.customer_index.clear()

        for account_data in data.get(
            "accounts",
            []
        ):
            account = Account(
                id=account_data["id"],
                customer_name=account_data[
                    "customer_name"
                ],
                balance=account_data["balance"]
            )

            self.accounts[account.id] = account

            self.customer_index[
                account.customer_name.lower()
            ].append(account.id)

        for transaction_data in data.get(
            "transactions",
            []
        ):
            transaction = Transaction(
                transaction_id=transaction_data[
                    "transaction_id"
                ],
                transaction_type=transaction_data[
                    "transaction_type"
                ],
                amount=transaction_data["amount"],
                related_account_id=transaction_data.get(
                    "related_account_id"
                ),
                reversed=transaction_data.get(
                    "reversed",
                    False
                )
            )

            self.transactions[
                transaction_data["account_id"]
            ].append(transaction)