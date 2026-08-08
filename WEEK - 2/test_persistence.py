import json

from bank import Bank
from storage_manager import DATA_FILE


def reset_storage():
    data = {
        "next_account_id": 1,
        "next_transaction_id": 1,
        "accounts": [],
        "transactions": []
    }

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )


def test_account_persistence():

    reset_storage()

    bank = Bank(persistent=True)

    account = bank.create_account(
        "Sivanesh",
        5000
    )

    account_id = account.id

    bank.deposit(
        account_id,
        1500
    )

    bank.withdraw(
        account_id,
        500
    )

    # Simulate closing the application.
    del bank

    # Create a new Bank instance.
    # This simulates starting the application again.
    new_bank = Bank(
        persistent=True
    )

    restored_account = new_bank.get_account(
        account_id
    )

    assert restored_account.customer_name == "Sivanesh"
    assert restored_account.balance == 6000

    history = new_bank.get_transaction_history(
        account_id
    )

    assert len(history) == 2

    assert history[0].transaction_type == "deposit"
    assert history[1].transaction_type == "withdraw"


def test_transaction_id_persistence():

    reset_storage()

    bank = Bank(
        persistent=True
    )

    account = bank.create_account(
        "Arun",
        3000
    )

    bank.deposit(
        account.id,
        500
    )

    del bank

    new_bank = Bank(
        persistent=True
    )

    restored_account = new_bank.get_account(
        account.id
    )

    new_bank.deposit(
        restored_account.id,
        1000
    )

    history = new_bank.get_transaction_history(
        restored_account.id
    )

    transaction_ids = [
        transaction.transaction_id
        for transaction in history
    ]

    assert transaction_ids == [1, 2]


def test_customer_index_persistence():

    reset_storage()

    bank = Bank(
        persistent=True
    )

    bank.create_account(
        "Kumar",
        2000
    )

    bank.create_account(
        "Kumar",
        3000
    )

    del bank

    new_bank = Bank(
        persistent=True
    )

    accounts = (
        new_bank.find_accounts_by_customer(
            "KUMAR"
        )
    )

    assert len(accounts) == 2


def run_tests():

    tests = [
        (
            "Account and transaction persistence",
            test_account_persistence
        ),
        (
            "Transaction ID persistence",
            test_transaction_id_persistence
        ),
        (
            "Customer index persistence",
            test_customer_index_persistence
        )
    ]

    print(
        "\n===== SECUREBANK PERSISTENCE TESTS =====\n"
    )

    passed = 0

    for name, test_function in tests:

        try:
            test_function()

            print(
                f"{name}: PASS"
            )

            passed += 1

        except Exception as error:

            print(
                f"{name}: FAIL"
            )

            print(
                "  Error:",
                repr(error)
            )

    print(
        f"\nResult: {passed}/{len(tests)} tests passed."
    )


if __name__ == "__main__":
    run_tests()