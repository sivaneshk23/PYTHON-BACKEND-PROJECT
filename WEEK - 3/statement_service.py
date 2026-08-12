from bisect import bisect_left, bisect_right, insort
from datetime import datetime
from typing import Any

from sortedcontainers import SortedDict


class StatementService:
    """
    Week 3 sorted account and transaction statement support.

    Responsibilities:
    - Maintain account IDs in sorted order using bisect.
    - Sort account views by ID and balance.
    - Maintain each account's transactions in a SortedDict.
    - Preserve transaction ordering using timestamp + transaction ID.
    """

    def __init__(self) -> None:
        self._sorted_account_ids: list[int] = []

        self._transaction_history: dict[
            int,
            SortedDict[tuple[datetime, int], Any]
        ] = {}

    # ------------------------------------------------------------------
    # Account sorting using bisect
    # ------------------------------------------------------------------

    def add_account_id(self, account_id: int) -> None:
        """
        Insert an account ID into the sorted ID list.

        bisect.insort() finds the insertion position efficiently,
        but inserting into a Python list still requires shifting
        existing elements.
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

        Account ID is used as a deterministic tie-breaker
        when two accounts have the same balance.
        """
        return sorted(
            accounts.values(),
            key=lambda account: (
                account.balance,
                account.id
            )
        )

    # ------------------------------------------------------------------
    # Transaction history using SortedDict
    # ------------------------------------------------------------------

    def _get_history(
        self,
        account_id: int
    ) -> SortedDict[tuple[datetime, int], Any]:
        """
        Get or create the SortedDict for one account.
        """
        if account_id not in self._transaction_history:
            self._transaction_history[account_id] = SortedDict()

        return self._transaction_history[account_id]

    def add_transaction(
        self,
        account_id: int,
        transaction: Any,
        timestamp: datetime
    ) -> None:
        """
        Store a transaction in sorted order.

        The key is:

            (timestamp, transaction_id)

        The timestamp provides chronological ordering.

        The transaction ID is the tie-breaker. This is essential
        because two transactions can occur at exactly the same
        timestamp. Using timestamp alone would cause the later
        transaction to replace the earlier one in SortedDict.
        """
        if not isinstance(timestamp, datetime):
            raise TypeError(
                "timestamp must be a datetime instance."
            )

        transaction_id = getattr(
            transaction,
            "transaction_id",
            None
        )

        if not isinstance(transaction_id, int):
            raise ValueError(
                "transaction must contain an integer transaction_id."
            )

        history = self._get_history(account_id)

        key = (
            timestamp,
            transaction_id
        )

        history[key] = transaction

    def get_sorted_transactions(
        self,
        account_id: int
    ) -> list[Any]:
        """
        Return all transactions for an account in chronological order.
        """
        history = self._transaction_history.get(
            account_id,
            SortedDict()
        )

        return list(history.values())

    def get_transaction_keys(
        self,
        account_id: int
    ) -> list[tuple[datetime, int]]:
        """
        Return the timestamp + transaction ID keys in sorted order.

        This method is useful for demonstrating how the tie-breaker
        works internally.
        """
        history = self._transaction_history.get(
            account_id,
            SortedDict()
        )

        return list(history.keys())

    def get_transaction_range(
    self,
    account_id: int,
    start_key: tuple[datetime, int],
    end_key: tuple[datetime, int]
) -> list[Any]:
        """
        Return transactions inside an inclusive SortedDict key range.

        The range is selected directly through SortedDict.irange().
        No manual filtering is performed.
        """
        history = self._transaction_history.get(
            account_id,
            SortedDict()
        )

        keys = history.irange(
            minimum=start_key,
            maximum=end_key,
            inclusive=(True, True)
        )

        return [history[key] for key in keys]
    def get_statement_between_dates(
    self,
    account_id: int,
    start_date: datetime,
    end_date: datetime
) -> list[Any]:
        """
        Return all transactions between two dates inclusively.

        The transaction history is already ordered by
        (timestamp, transaction_id), so the requested range is
        delegated directly to SortedDict.irange().
        """
        if start_date > end_date:
            raise ValueError(
                "start_date must not be later than end_date."
            )

        start_key = (
            start_date,
            -1
        )

        end_key = (
        end_date,
        2**63 - 1
        )

        return self.get_transaction_range(
            account_id,
            start_key,
            end_key
        )