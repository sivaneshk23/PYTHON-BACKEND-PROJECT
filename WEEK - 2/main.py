from bank import (
    Bank,
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError
)


bank = Bank()


while True:
    print("\n===== SECUREBANK - WEEK 2 =====")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Transfer Money")
    print("6. Reverse Last Transaction")
    print("7. Find Accounts by Customer")
    print("8. View Transaction History")
    print("9. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            name = input("Enter customer name: ")

            initial_balance = float(
                input("Enter initial balance: Rs.")
            )

            account = bank.create_account(
                name,
                initial_balance
            )

            print("\nAccount created successfully!")
            print("Account ID:", account.id)
            print(
                "Customer Name:",
                account.customer_name
            )
            print(
                f"Balance: Rs.{account.balance:.2f}"
            )

        elif choice == "2":
            account_id = int(
                input("Enter account ID: ")
            )

            amount = float(
                input("Enter deposit amount: Rs.")
            )

            bank.deposit(
                account_id,
                amount
            )

            print("Deposit successful.")

            print(
                f"Current Balance: "
                f"Rs.{bank.get_balance(account_id):.2f}"
            )

        elif choice == "3":
            account_id = int(
                input("Enter account ID: ")
            )

            amount = float(
                input("Enter withdrawal amount: Rs.")
            )

            bank.withdraw(
                account_id,
                amount
            )

            print("Withdrawal successful.")

            print(
                f"Current Balance: "
                f"Rs.{bank.get_balance(account_id):.2f}"
            )

        elif choice == "4":
            account_id = int(
                input("Enter account ID: ")
            )

            print(
                f"Current Balance: "
                f"Rs.{bank.get_balance(account_id):.2f}"
            )

        elif choice == "5":
            from_id = int(
                input("Enter sender account ID: ")
            )

            to_id = int(
                input("Enter receiver account ID: ")
            )

            amount = float(
                input("Enter transfer amount: Rs.")
            )

            bank.transfer(
                from_id,
                to_id,
                amount
            )

            print("Transfer successful.")

            print(
                f"Sender Balance: "
                f"Rs.{bank.get_balance(from_id):.2f}"
            )

            print(
                f"Receiver Balance: "
                f"Rs.{bank.get_balance(to_id):.2f}"
            )

        elif choice == "6":
            account_id = int(
                input("Enter account ID: ")
            )

            bank.reverse_last_transaction(
                account_id
            )

            print(
                "Last transaction reversed successfully."
            )

            print(
                f"Current Balance: "
                f"Rs.{bank.get_balance(account_id):.2f}"
            )

        elif choice == "7":
            name = input(
                "Enter customer name: "
            )

            accounts = (
                bank.find_accounts_by_customer(name)
            )

            if not accounts:
                print("No accounts found.")

            else:
                print("\nAccounts found:")

                for account in accounts:
                    print(
                        f"ID: {account.id} | "
                        f"Name: {account.customer_name} | "
                        f"Balance: Rs.{account.balance:.2f}"
                    )

        elif choice == "8":
            account_id = int(
                input("Enter account ID: ")
            )

            transactions = (
                bank.get_transaction_history(
                    account_id
                )
            )

            if not transactions:
                print(
                    "No transactions found."
                )

            else:
                print(
                    "\n===== TRANSACTION HISTORY ====="
                )

                for transaction in transactions:
                    print(
                        f"ID: {transaction.transaction_id} | "
                        f"Type: {transaction.transaction_type} | "
                        f"Amount: Rs.{transaction.amount:.2f} | "
                        f"Related Account: "
                        f"{transaction.related_account_id} | "
                        f"Reversed: {transaction.reversed}"
                    )

        elif choice == "9":
            print(
                "Thank you for using SecureBank."
            )
            break

        else:
            print(
                "Invalid choice. "
                "Please select from 1 to 9."
            )

    except (
        AccountNotFoundError,
        InsufficientFundsError,
        InvalidAmountError,
        ValueError
    ) as error:
        print("Error:", error)