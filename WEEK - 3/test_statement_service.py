from dataclasses import dataclass

from statement_service import StatementService


@dataclass
class FakeAccount:
    id: int
    customer_name: str
    balance: float


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