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
    print("8. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            name = input("Enter customer name: ")
            initial_balance = float(
                input("Enter initial balance: ₹")
            )

            account = bank.create_account(
                name,
                initial_balance
            )

            print("\nAccount created successfully!")
            print("Account ID:", account.id)
            print("Customer Name:", account.customer_name)
            print(f"Balance: ₹{account.balance:.2f}")

        elif choice == "2":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter deposit amount: ₹"))

            bank.deposit(account_id, amount)

            print("Deposit successful.")
            print(
                f"Current Balance: ₹{bank.get_balance(account_id):.2f}"
            )

        elif choice == "3":
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter withdrawal amount: ₹"))

            bank.withdraw(account_id, amount)

            print("Withdrawal successful.")
            print(
                f"Current Balance: ₹{bank.get_balance(account_id):.2f}"
            )

        elif choice == "4":
            account_id = int(input("Enter account ID: "))

            print(
                f"Current Balance: ₹{bank.get_balance(account_id):.2f}"
            )

        elif choice == "5":
            from_id = int(input("Enter sender account ID: "))
            to_id = int(input("Enter receiver account ID: "))
            amount = float(input("Enter transfer amount: ₹"))

            bank.transfer(from_id, to_id, amount)

            print("Transfer successful.")

            print(
                f"Sender Balance: ₹{bank.get_balance(from_id):.2f}"
            )

            print(
                f"Receiver Balance: ₹{bank.get_balance(to_id):.2f}"
            )

        elif choice == "6":
            account_id = int(input("Enter account ID: "))

            bank.reverse_last_transaction(account_id)

            print("Last transaction reversed successfully.")

            print(
                f"Current Balance: ₹{bank.get_balance(account_id):.2f}"
            )

        elif choice == "7":
            name = input("Enter customer name: ")

            accounts = bank.find_accounts_by_customer(name)

            if not accounts:
                print("No accounts found.")

            else:
                print("\nAccounts found:")

                for account in accounts:
                    print(
                        f"ID: {account.id} | "
                        f"Name: {account.customer_name} | "
                        f"Balance: ₹{account.balance:.2f}"
                    )

        elif choice == "8":
            print("Thank you for using SecureBank.")
            break

        else:
            print("Invalid choice. Please select from 1 to 8.")

    except (
        AccountNotFoundError,
        InsufficientFundsError,
        InvalidAmountError,
        ValueError
    ) as error:
        print("Error:", error)