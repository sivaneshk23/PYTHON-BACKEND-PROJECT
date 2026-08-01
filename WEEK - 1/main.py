from bank import (
    create_account,
    deposit,
    withdraw,
    check_balance,
    close_account
)

from exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError
)


while True:

    print("\n===== SECUREBANK =====")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Close Account")
    print("6. Exit")

    choice = input("Enter your choice: ")

    try:

        if choice == "1":

            name = input("Enter customer name: ")

            account = create_account(name)

            print("\nAccount created successfully!")
            print("Account ID:", account.id)
            print("Customer Name:", account.customer_name)


        elif choice == "2":

            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter deposit amount: "))

            balance = deposit(account_id, amount)

            print("Deposit successful.")
            print(f"Current Balance: ₹{balance:.2f}")


        elif choice == "3":

            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter withdrawal amount: "))

            balance = withdraw(account_id, amount)

            print("Withdrawal successful.")
            print(f"Current Balance: ₹{balance:.2f}")


        elif choice == "4":

            account_id = int(input("Enter account ID: "))

            balance = check_balance(account_id)

            print(f"Current Balance: ₹{balance:.2f}")


        elif choice == "5":

            account_id = int(input("Enter account ID: "))

            account = close_account(account_id)

            print(
                f"Account {account.id} belonging to "
                f"{account.customer_name} closed successfully."
            )


        elif choice == "6":

            print("Thank you for using SecureBank.")
            break


        else:

            print("Invalid choice. Please select from 1 to 6.")


    except AccountNotFoundError as e:
        print("Error:", e)

    except InsufficientFundsError as e:
        print("Error:", e)

    except InvalidAmountError as e:
        print("Error:", e)

    except ValueError as e:
        print("Error:", e)