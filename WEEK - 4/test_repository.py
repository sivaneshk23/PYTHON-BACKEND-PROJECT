from persistence import AccountRecord
from repository import (
    AccountRepository,
    InMemoryAccountRepository,
)


def create_account(
    account_id: int,
    customer_name: str,
    balance: float,
) -> AccountRecord:
    return AccountRecord(
        account_id=account_id,
        customer_name=customer_name,
        balance=balance,
    )


def test_in_memory_repository_implements_repository_contract():
    repository = InMemoryAccountRepository()

    assert isinstance(
        repository,
        AccountRepository,
    )


def test_save_and_get_account():
    repository = InMemoryAccountRepository()

    account = create_account(
        1001,
        "Sivanesh",
        5000.0,
    )

    repository.save(account)

    result = repository.get(1001)

    assert result == account


def test_get_missing_account_returns_none():
    repository = InMemoryAccountRepository()

    result = repository.get(9999)

    assert result is None


def test_list_returns_all_accounts():
    repository = InMemoryAccountRepository()

    account_1 = create_account(
        1001,
        "Sivanesh",
        5000.0,
    )

    account_2 = create_account(
        1002,
        "Kumar",
        2500.0,
    )

    repository.save(account_1)
    repository.save(account_2)

    result = repository.list()

    assert result == [
        account_1,
        account_2,
    ]


def test_save_updates_existing_account():
    repository = InMemoryAccountRepository()

    account = create_account(
        1001,
        "Sivanesh",
        5000.0,
    )

    updated_account = create_account(
        1001,
        "Sivanesh",
        7500.0,
    )

    repository.save(account)
    repository.save(updated_account)

    assert repository.get(1001) == updated_account
    assert len(repository.list()) == 1


def test_delete_existing_account_returns_true():
    repository = InMemoryAccountRepository()

    account = create_account(
        1001,
        "Sivanesh",
        5000.0,
    )

    repository.save(account)

    result = repository.delete(1001)

    assert result is True
    assert repository.get(1001) is None


def test_delete_missing_account_returns_false():
    repository = InMemoryAccountRepository()

    result = repository.delete(9999)

    assert result is False