from bank import (
    Bank,
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError
)


def test_transfer_reversal():
    bank = Bank()

    sender = bank.create_account(
        "Arun",
        5000
    )

    receiver = bank.create_account(
        "Priya",
        3000
    )

    bank.transfer(
        sender.id,
        receiver.id,
        1000
    )

    assert sender.balance == 4000
    assert receiver.balance == 4000

    bank.reverse_last_transaction(
        sender.id
    )

    assert sender.balance == 5000
    assert receiver.balance == 3000

    sender_transactions = (
        bank.get_transaction_history(sender.id)
    )

    receiver_transactions = (
        bank.get_transaction_history(receiver.id)
    )

    assert sender_transactions[0].reversed is True
    assert receiver_transactions[0].reversed is True

    assert (
        sender_transactions[-1].transaction_type
        == "transfer_reversal_in"
    )

    assert (
        receiver_transactions[-1].transaction_type
        == "transfer_reversal_out"
    )


def test_transfer_reversal_insufficient_receiver_balance():
    bank = Bank()

    sender = bank.create_account(
        "Arun",
        5000
    )

    receiver = bank.create_account(
        "Priya",
        1000
    )

    bank.transfer(
        sender.id,
        receiver.id,
        1000
    )

    # Receiver now has 2000.
    receiver.balance = 500

    sender_before = sender.balance
    receiver_before = receiver.balance

    try:
        bank.reverse_last_transaction(
            sender.id
        )

        assert False

    except InsufficientFundsError:
        pass

    assert sender.balance == sender_before
    assert receiver.balance == receiver_before


def test_same_account_transfer():
    bank = Bank()

    account = bank.create_account(
        "Kumar",
        5000
    )

    balance_before = account.balance

    try:
        bank.transfer(
            account.id,
            account.id,
            1000
        )

        assert False

    except ValueError:
        pass

    assert account.balance == balance_before


def test_invalid_amounts():
    bank = Bank()

    account = bank.create_account(
        "Meena",
        5000
    )

    invalid_operations = [
        lambda: bank.deposit(
            account.id,
            0
        ),
        lambda: bank.deposit(
            account.id,
            -100
        ),
        lambda: bank.withdraw(
            account.id,
            0
        ),
        lambda: bank.withdraw(
            account.id,
            -100
        )
    ]

    for operation in invalid_operations:

        try:
            operation()

            assert False

        except InvalidAmountError:
            pass

    assert account.balance == 5000


def test_insufficient_withdrawal():
    bank = Bank()

    account = bank.create_account(
        "Rahul",
        1000
    )

    try:
        bank.withdraw(
            account.id,
            2000
        )

        assert False

    except InsufficientFundsError:
        pass

    assert account.balance == 1000


def test_nonexistent_account():
    bank = Bank()

    try:
        bank.get_balance(999)

        assert False

    except AccountNotFoundError:
        pass


def test_case_insensitive_customer_search():
    bank = Bank()

    bank.create_account(
        "Sivanesh",
        2000
    )

    bank.create_account(
        "Sivanesh",
        3000
    )

    lowercase_result = (
        bank.find_accounts_by_customer(
            "sivanesh"
        )
    )

    uppercase_result = (
        bank.find_accounts_by_customer(
            "SIVANESH"
        )
    )

    assert len(lowercase_result) == 2
    assert len(uppercase_result) == 2


def run_tests():

    tests = [
        (
            "Transfer reversal",
            test_transfer_reversal
        ),
        (
            "Unsafe transfer reversal protection",
            test_transfer_reversal_insufficient_receiver_balance
        ),
        (
            "Same-account transfer protection",
            test_same_account_transfer
        ),
        (
            "Invalid amount validation",
            test_invalid_amounts
        ),
        (
            "Insufficient withdrawal protection",
            test_insufficient_withdrawal
        ),
        (
            "Non-existent account handling",
            test_nonexistent_account
        ),
        (
            "Case-insensitive customer indexing",
            test_case_insensitive_customer_search
        )
    ]

    print(
        "\n===== SECUREBANK EDGE-CASE TESTS =====\n"
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
        f"\nResult: {passed}/{len(tests)} "
        "tests passed."
    )


if __name__ == "__main__":
    run_tests()