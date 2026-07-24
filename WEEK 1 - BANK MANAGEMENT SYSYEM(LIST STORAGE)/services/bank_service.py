from models.account import Account


class BankService:

    def __init__(self):
        self.accounts = []

    def create_account(self):

        account_id = input("Enter Account ID : ")

        for account in self.accounts:
            if account.account_id == account_id:
                print("Account ID already exists.")
                return

        name = input("Enter Name : ")

        balance = float(input("Enter Initial Deposit : "))

        account = Account(account_id, name, balance)

        self.accounts.append(account)

        print("Account Created Successfully.")

    def find_account(self, account_id):

        for account in self.accounts:
            if account.account_id == account_id:
                return account

        return None

    def deposit(self):

        account_id = input("Enter Account ID : ")

        account = self.find_account(account_id)

        if account:

            amount = float(input("Enter Deposit Amount : "))

            account.deposit(amount)

            print("Amount Deposited Successfully.")

        else:

            print("Account Not Found.")

    def withdraw(self):

        account_id = input("Enter Account ID : ")

        account = self.find_account(account_id)

        if account:

            amount = float(input("Enter Withdraw Amount : "))

            if account.withdraw(amount):
                print("Withdrawal Successful.")
            else:
                print("Insufficient Balance.")

        else:

            print("Account Not Found.")

    def balance_check(self):

        account_id = input("Enter Account ID : ")

        account = self.find_account(account_id)

        if account:
            print("Current Balance :", account.balance)
        else:
            print("Account Not Found.")

    def view_accounts(self):

        if len(self.accounts) == 0:
            print("No Accounts Available.")
            return

        print()

        print("AccountID\tName\tBalance")

        for account in self.accounts:
            print(account.account_id, "\t", account.name, "\t", account.balance)