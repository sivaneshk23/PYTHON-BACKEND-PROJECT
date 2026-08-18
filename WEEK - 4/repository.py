from abc import ABC, abstractmethod
from typing import Optional

from persistence import AccountRecord


class AccountRepository(ABC):

    @abstractmethod
    def save(self, account: AccountRecord) -> None:
        pass

    @abstractmethod
    def get(
        self,
        account_id: int,
    ) -> Optional[AccountRecord]:
        pass

    @abstractmethod
    def list(self) -> list[AccountRecord]:
        pass

    @abstractmethod
    def delete(self, account_id: int) -> bool:
        pass


class InMemoryAccountRepository(AccountRepository):

    def __init__(self) -> None:
        self._accounts: dict[int, AccountRecord] = {}

    def save(self, account: AccountRecord) -> None:
        self._accounts[account.account_id] = account

    def get(
        self,
        account_id: int,
    ) -> Optional[AccountRecord]:
        return self._accounts.get(account_id)

    def list(self) -> list[AccountRecord]:
        return list(self._accounts.values())

    def delete(self, account_id: int) -> bool:
        if account_id not in self._accounts:
            return False

        del self._accounts[account_id]
        return True