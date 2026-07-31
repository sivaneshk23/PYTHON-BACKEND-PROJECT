from services.bank_service import BankService
from utils.menu import display_menu


bank = BankService()

while True:

    display_menu()

    choice = input("Enter Choice : ")

    if choice == "1":

        bank.create_account()

    elif choice == "2":

        bank.deposit()

    elif choice == "3":

        bank.withdraw()

    elif choice == "4":

        bank.balance_check()

    elif choice == "5":

        bank.view_accounts()

    elif choice == "6":

        print("Thank You")
        break

    else:

        print("Invalid Choice")