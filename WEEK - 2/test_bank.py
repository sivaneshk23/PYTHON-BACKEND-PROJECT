from bank import (
    Bank,
    AccountNotFoundError
)


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name}: {status}")


# ============================================================
# TEST 1 - CONSERVATION OF MONEY DURING TRANSFER
# ============================================================

def test_transfer_conservation():
    bank = Bank()

    account_a = bank.create_account("Arun", 5000)
    account_b = bank.create_account("Priya", 3000)

    total_before = account_a.balance + account_b.balance

    bank.transfer(
        account_a.id,
        account_b.id,
        1000
    )

    total_after = account_a.balance + account_b.balance

    assert account_a.balance == 4000
    assert account_b.balance == 4000
    assert total_before == total_after


# ============================================================
# TEST 2 - FAILED TRANSFER MUST NOT DEBIT SENDER
# ============================================================

def test_failed_transfer_rollback():
    bank = Bank()

    sender = bank.create_account("Sivanesh", 5000)

    balance_before = sender.balance

    try:
        bank.transfer(
            sender.id,
            999,
            1000
        )

    except AccountNotFoundError:
        pass

    balance_after = sender.balance

    assert balance_before == balance_after
    assert sender.balance == 5000


# ============================================================
# TEST 3 - CUSTOMER SECONDARY INDEX
# ============================================================

def test_customer_index():
    bank = Bank()

    first_account = bank.create_account(
        "Kumar",
        2000
    )

    second_account = bank.create_account(
        "Kumar",
        4000
    )

    accounts = bank.find_accounts_by_customer(
        "Kumar"
    )

    assert len(accounts) == 2

    account_ids = [
        account.id
        for account in accounts
    ]

    assert first_account.id in account_ids
    assert second_account.id in account_ids


# ============================================================
# TEST 4 - REVERSE EXACTLY ONE DEPOSIT
# ============================================================

def test_reverse_last_transaction():
    bank = Bank()

    account = bank.create_account(
        "Meena",
        5000
    )

    bank.deposit(
        account.id,
        1000
    )

    bank.deposit(
        account.id,
        500
    )

    assert account.balance == 6500

    bank.reverse_last_transaction(
        account.id
    )

    # Only the latest ₹500 deposit must be reversed.
    assert account.balance == 6000

    transactions = bank.transactions[account.id]

    # First ₹1000 deposit must remain active.
    assert transactions[0].amount == 1000
    assert transactions[0].reversed is False

    # Latest ₹500 deposit must be marked as reversed.
    assert transactions[1].amount == 500
    assert transactions[1].reversed is True

    # A reversal record must be preserved in history.
    assert transactions[2].transaction_type == "deposit_reversal"
    assert transactions[2].amount == 500


# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":

    tests = [
        (
            "Transfer conservation test",
            test_transfer_conservation
        ),
        (
            "Failed transfer rollback test",
            test_failed_transfer_rollback
        ),
        (
            "Customer secondary index test",
            test_customer_index
        ),
        (
            "Single transaction reversal test",
            test_reverse_last_transaction
        )
    ]

    print("\n===== SECUREBANK WEEK 2 TESTS =====\n")

    passed_count = 0

    for test_name, test_function in tests:

        try:
            test_function()

            print_result(
                test_name,
                True
            )

            passed_count += 1

        except Exception as error:

            print_result(
                test_name,
                False
            )

            print(
                "  Error:",
                error
            )

    print(
        f"\nResult: {passed_count}/{len(tests)} tests passed."
    )