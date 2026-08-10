from bisect import bisect_left, bisect_right, insort
from typing import Any


class StatementService:
    """
    Week 3 sorted account and statement support.

    This service is responsible for:
    - maintaining sorted account IDs using bisect
    - producing accounts sorted by ID
    - producing accounts sorted by balance
    """

    def __init__(self) -> None:
        self._sorted_account_ids: list[int] = []

    def add_account_id(self, account_id: int) -> None:
        """
        Insert an account ID into the sorted ID list.

        bisect.insort() performs a binary search to find the
        insertion position, but inserting into the Python list
        still requires shifting elements.
        """
        if account_id not in self._sorted_account_ids:
            insort(self._sorted_account_ids, account_id)

    def remove_account_id(self, account_id: int) -> None:
        """
        Remove an account ID using bisect-based lookup.
        """
        position = bisect_left(
            self._sorted_account_ids,
            account_id
        )

        if (
            position < len(self._sorted_account_ids)
            and self._sorted_account_ids[position] == account_id
        ):
            self._sorted_account_ids.pop(position)

    def contains_account_id(self, account_id: int) -> bool:
        """
        Check whether an account ID exists using bisect.
        """
        position = bisect_left(
            self._sorted_account_ids,
            account_id
        )

        return (
            position < len(self._sorted_account_ids)
            and self._sorted_account_ids[position] == account_id
        )

    def get_sorted_account_ids(self) -> list[int]:
        """
        Return account IDs in ascending order.
        """
        return self._sorted_account_ids.copy()

    def get_account_ids_in_range(
        self,
        lower_id: int,
        upper_id: int
    ) -> list[int]:
        """
        Return account IDs within an inclusive range.

        bisect_left() finds the first valid position.
        bisect_right() finds the position immediately after
        the last valid position.

        No manual filtering loop is used.
        """
        start = bisect_left(
            self._sorted_account_ids,
            lower_id
        )

        end = bisect_right(
            self._sorted_account_ids,
            upper_id
        )

        return self._sorted_account_ids[start:end]

    def sort_accounts_by_id(
        self,
        accounts: dict[int, Any]
    ) -> list[Any]:
        """
        Return account objects sorted by account ID.

        The ordering comes from the bisect-maintained ID list.
        """
        return [
            accounts[account_id]
            for account_id in self._sorted_account_ids
            if account_id in accounts
        ]

    def sort_accounts_by_balance(
        self,
        accounts: dict[int, Any]
    ) -> list[Any]:
        """
        Return account objects sorted by balance.

        Account ID is used as a deterministic tie-breaker when
        two accounts have the same balance.
        """
        return sorted(
            accounts.values(),
            key=lambda account: (
                account.balance,
                account.id
            )
        )