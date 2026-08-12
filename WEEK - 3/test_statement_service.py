from dataclasses import dataclass
from datetime import datetime

from statement_service import StatementService


@dataclass
class FakeAccount:
    id: int
    customer_name: str
    balance: float


@dataclass
class FakeTransaction:
    transaction_id: int
    transaction_type: str
    amount: float


# ----------------------------------------------------------------------
# Account sorting tests
# ----------------------------------------------------------------------


def test_account_ids_are_kept_sorted():
    service = StatementService()

    service.add_account_id(105)
    service.add_account_id(101)
    service.add_account_id(110)
    service.add_account_id(103)

    assert service.get_sorted_account_ids() == [
        101,
        103,
        105,
        110
    ]


def test_duplicate_account_id_is_not_inserted_twice():
    service = StatementService()

    service.add_account_id(101)
    service.add_account_id(101)

    assert service.get_sorted_account_ids() == [101]


def test_account_id_range_uses_correct_boundaries():
    service = StatementService()

    for account_id in [101, 103, 105, 110]:
        service.add_account_id(account_id)

    assert service.get_account_ids_in_range(
        100,
        108
    ) == [101, 103, 105]


def test_account_id_existence():
    service = StatementService()

    service.add_account_id(101)

    assert service.contains_account_id(101)
    assert not service.contains_account_id(999)


def test_account_id_removal():
    service = StatementService()

    for account_id in [101, 103, 105]:
        service.add_account_id(account_id)

    service.remove_account_id(103)

    assert service.get_sorted_account_ids() == [
        101,
        105
    ]


def test_accounts_can_be_sorted_by_id():
    service = StatementService()

    accounts = {
        105: FakeAccount(105, "Charlie", 5000),
        101: FakeAccount(101, "Alice", 9000),
        103: FakeAccount(103, "Bob", 3000),
    }

    for account_id in accounts:
        service.add_account_id(account_id)

    result = service.sort_accounts_by_id(accounts)

    assert [account.id for account in result] == [
        101,
        103,
        105
    ]


def test_accounts_can_be_sorted_by_balance():
    service = StatementService()

    accounts = {
        105: FakeAccount(105, "Charlie", 5000),
        101: FakeAccount(101, "Alice", 9000),
        103: FakeAccount(103, "Bob", 3000),
    }

    for account_id in accounts:
        service.add_account_id(account_id)

    result = service.sort_accounts_by_balance(accounts)

    assert [account.id for account in result] == [
        103,
        105,
        101
    ]


# ----------------------------------------------------------------------
# SortedDict transaction tests
# ----------------------------------------------------------------------


def test_transactions_are_sorted_by_timestamp():
    service = StatementService()

    timestamp_1 = datetime(
        2026, 8, 11, 10, 0, 0
    )

    timestamp_2 = datetime(
        2026, 8, 11, 11, 0, 0
    )

    timestamp_3 = datetime(
        2026, 8, 11, 12, 0, 0
    )

    transaction_1 = FakeTransaction(
        transaction_id=1,
        transaction_type="deposit",
        amount=5000
    )

    transaction_2 = FakeTransaction(
        transaction_id=2,
        transaction_type="withdraw",
        amount=1000
    )

    transaction_3 = FakeTransaction(
        transaction_id=3,
        transaction_type="deposit",
        amount=2000
    )

    service.add_transaction(
        101,
        transaction_3,
        timestamp_3
    )

    service.add_transaction(
        101,
        transaction_1,
        timestamp_1
    )

    service.add_transaction(
        101,
        transaction_2,
        timestamp_2
    )

    result = service.get_sorted_transactions(101)

    assert [
        transaction.transaction_id
        for transaction in result
    ] == [1, 2, 3]


def test_same_timestamp_transactions_are_not_overwritten():
    service = StatementService()

    same_timestamp = datetime(
        2026, 8, 11, 10, 30, 0
    )

    transaction_1 = FakeTransaction(
        transaction_id=1,
        transaction_type="deposit",
        amount=5000
    )

    transaction_2 = FakeTransaction(
        transaction_id=2,
        transaction_type="withdraw",
        amount=1000
    )

    service.add_transaction(
        101,
        transaction_1,
        same_timestamp
    )

    service.add_transaction(
        101,
        transaction_2,
        same_timestamp
    )

    result = service.get_sorted_transactions(101)

    assert len(result) == 2

    assert [
        transaction.transaction_id
        for transaction in result
    ] == [1, 2]


def test_transaction_key_contains_timestamp_and_tie_breaker():
    service = StatementService()

    timestamp = datetime(
        2026, 8, 11, 10, 30, 0
    )

    transaction_1 = FakeTransaction(
        transaction_id=1,
        transaction_type="deposit",
        amount=5000
    )

    transaction_2 = FakeTransaction(
        transaction_id=2,
        transaction_type="deposit",
        amount=2000
    )

    service.add_transaction(
        101,
        transaction_1,
        timestamp
    )

    service.add_transaction(
        101,
        transaction_2,
        timestamp
    )

    keys = service.get_transaction_keys(101)

    assert keys == [
        (timestamp, 1),
        (timestamp, 2)
    ]


def test_transactions_can_be_retrieved_for_a_key_range():
    service = StatementService()

    timestamp_1 = datetime(
        2026, 1, 1, 10, 0, 0
    )

    timestamp_2 = datetime(
        2026, 1, 10, 10, 0, 0
    )

    timestamp_3 = datetime(
        2026, 1, 20, 10, 0, 0
    )

    transaction_1 = FakeTransaction(
        transaction_id=1,
        transaction_type="deposit",
        amount=1000
    )

    transaction_2 = FakeTransaction(
        transaction_id=2,
        transaction_type="deposit",
        amount=2000
    )

    transaction_3 = FakeTransaction(
        transaction_id=3,
        transaction_type="withdraw",
        amount=500
    )

    service.add_transaction(
        101,
        transaction_1,
        timestamp_1
    )

    service.add_transaction(
        101,
        transaction_2,
        timestamp_2
    )

    service.add_transaction(
        101,
        transaction_3,
        timestamp_3
    )

    result = service.get_transaction_range(
        101,
        (timestamp_1, 1),
        (timestamp_2, 2)
    )

    assert [
        transaction.transaction_id
        for transaction in result
    ] == [1, 2]
def test_statement_returns_only_transactions_inside_date_range():
    service = StatementService()

    transaction_1_date = datetime(
        2026, 1, 1, 10, 0, 0
    )

    transaction_2_date = datetime(
        2026, 1, 5, 10, 0, 0
    )

    transaction_3_date = datetime(
        2026, 1, 10, 10, 0, 0
    )

    transaction_4_date = datetime(
        2026, 1, 20, 10, 0, 0
    )

    transaction_1 = FakeTransaction(
        transaction_id=1,
        transaction_type="deposit",
        amount=5000
    )

    transaction_2 = FakeTransaction(
        transaction_id=2,
        transaction_type="withdraw",
        amount=1000
    )

    transaction_3 = FakeTransaction(
        transaction_id=3,
        transaction_type="deposit",
        amount=2000
    )

    transaction_4 = FakeTransaction(
        transaction_id=4,
        transaction_type="withdraw",
        amount=500
    )

    service.add_transaction(
        101,
        transaction_1,
        transaction_1_date
    )

    service.add_transaction(
        101,
        transaction_2,
        transaction_2_date
    )

    service.add_transaction(
        101,
        transaction_3,
        transaction_3_date
    )

    service.add_transaction(
        101,
        transaction_4,
        transaction_4_date
    )

    result = service.get_statement_between_dates(
        101,
        datetime(2026, 1, 1),
        datetime(2026, 1, 15, 23, 59, 59)
    )

    assert [
        transaction.transaction_id
        for transaction in result
    ] == [1, 2, 3]


def test_statement_includes_transactions_on_boundary_dates():
    service = StatementService()

    start_date = datetime(
        2026, 1, 1, 0, 0, 0
    )

    end_date = datetime(
        2026, 1, 15, 23, 59, 59
    )

    transaction_1 = FakeTransaction(
        transaction_id=1,
        transaction_type="deposit",
        amount=1000
    )

    transaction_2 = FakeTransaction(
        transaction_id=2,
        transaction_type="deposit",
        amount=2000
    )

    service.add_transaction(
        101,
        transaction_1,
        start_date
    )

    service.add_transaction(
        101,
        transaction_2,
        end_date
    )

    result = service.get_statement_between_dates(
        101,
        start_date,
        end_date
    )

    assert [
        transaction.transaction_id
        for transaction in result
    ] == [1, 2]


def test_statement_rejects_reversed_date_range():
    service = StatementService()

    try:
        service.get_statement_between_dates(
            101,
            datetime(2026, 1, 15),
            datetime(2026, 1, 1)
        )
    except ValueError as error:
        assert str(error) == (
            "start_date must not be later than end_date."
        )
    else:
        raise AssertionError(
            "Expected ValueError for reversed date range."
        )