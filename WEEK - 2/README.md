# Week 2 — Transfers, Reversals & Multi-Key Customer Indexing

> SecureBank Python Backend — Week 2 implementation focused on atomic money transfers, transaction reversal, transaction history, and secondary customer indexing.

## 1. Week Overview

Week 2 extends the Week 1 in-memory SecureBank ledger with transaction-level business logic.

The implementation introduces money transfers between accounts, reversal of the latest transaction, transaction history, and a secondary customer-name index that allows all accounts belonging to a customer to be located efficiently.

The central engineering requirement of this week is **correctness during failure**. A failed transfer must never leave the sender partially debited. The implementation therefore treats the transfer as an atomic operation and uses manual rollback when necessary.

---

## 2. Week 2 Objectives

The objectives of Week 2 are to:

* Transfer money safely between two accounts.
* Preserve the total system balance during transfers.
* Prevent partial transfers when an operation fails.
* Record account transactions.
* Reverse exactly one latest transaction.
* Support multiple accounts belonging to the same customer.
* Build a secondary customer-name index.
* Handle invalid account IDs safely.
* Handle invalid transaction amounts safely.
* Demonstrate the implementation through automated tests and live verification.

---

## 3. Required Functionality

Week 2 implements the following functionality:

### 3.1 Money Transfer

Transfer money from one account to another.

Conceptually:

```text
transfer(from_id, to_id, amount)
```

The operation consists of:

```text
Source account
      ↓
Withdraw amount
      ↓
Target account
      ↓
Deposit amount
```

The operation must behave atomically.

If the second half fails, the first operation must be rolled back.

---

### 3.2 Transaction Logging

Every relevant account operation is recorded as a transaction.

The transaction history is associated with each account so that the system can identify the most recent transaction.

Transactions are represented using a Python `@dataclass`.

---

### 3.3 Transaction Reversal

The system supports reversal of the latest transaction for an account.

The reversal must undo exactly one transaction rather than incorrectly reversing multiple operations.

---

### 3.4 Customer Secondary Index

A secondary index is maintained using:

```python
collections.defaultdict(list)
```

The conceptual structure is:

```text
Customer Name
      ↓
List of Account IDs
```

Example:

```text
Alice
 ├── 101
 └── 103
```

This allows the system to find all accounts associated with the same customer without scanning the entire account collection.

---

## 4. Core Data Structures

### Account Storage

Accounts continue to use a dictionary:

```python
dict[int, Account]
```

This provides direct account lookup by account ID.

---

### Transaction Representation

Transactions use a dataclass containing the information required to describe an account operation.

Conceptually:

```python
@dataclass
class Transaction:
    ...
```

---

### Customer Index

The secondary customer index uses:

```python
defaultdict(list)
```

Conceptually:

```python
customer_index[customer_name].append(account_id)
```

This supports customers who own multiple accounts.

---

## 5. Transfer Atomicity

Atomicity is the most important correctness requirement of Week 2.

Consider:

```text
Account A = ₹5,000
Account B = ₹3,000
```

Transfer:

```text
₹1,000 from A → B
```

Expected:

```text
A = ₹4,000
B = ₹4,000
```

Total before:

```text
₹5,000 + ₹3,000 = ₹8,000
```

Total after:

```text
₹4,000 + ₹4,000 = ₹8,000
```

Therefore:

```text
Total balance before
=
Total balance after
```

This is the transfer conservation invariant.

---

## 6. Failed Transfer Protection

A transfer must not partially modify the sender.

Example:

```text
Sender balance = ₹5,000
Target account = does not exist
Transfer = ₹1,000
```

Incorrect behavior:

```text
Sender = ₹4,000
Target = invalid
```

This would permanently lose ₹1,000 from the sender.

Correct behavior:

```text
Sender = ₹5,000
Target = invalid
```

The sender must remain exactly as it was before the failed transfer.

This protects the system from the classic partial-transfer bug.

---

## 7. Rollback Strategy

The transfer implementation uses manual rollback with `try/except`.

The conceptual flow is:

```text
Validate source
      ↓
Validate target
      ↓
Store original state
      ↓
Withdraw from source
      ↓
Deposit into target
      ↓
Record transaction
```

If the operation fails after the source has been modified:

```text
Exception
   ↓
Restore original source state
   ↓
Restore original target state
   ↓
Report failure
```

This ensures a failed operation does not leave inconsistent account balances.

---

## 8. Customer Index Example

Suppose the system contains:

```text
Account 101 → Alice
Account 103 → Bob
Account 105 → Alice
```

The secondary index becomes conceptually:

```text
Alice → [101, 105]
Bob   → [103]
```

A customer lookup for Alice therefore returns:

```text
[101, 105]
```

The index must be updated whenever a new account is created.

---

## 9. Reversal Behavior

If an account has the following transaction history:

```text
1. Deposit ₹5,000
2. Withdraw ₹1,000
3. Deposit ₹2,000
```

The latest transaction is:

```text
Deposit ₹2,000
```

Calling:

```text
reverse_last_transaction(account_id)
```

must reverse only that latest operation.

The resulting state must correspond to the state immediately before transaction 3.

A second reversal should then target transaction 2 rather than incorrectly reversing transaction 3 again.

---

## 10. Validation Requirements

The implementation must reject invalid operations safely.

Examples include:

* Non-existent account ID
* Closed account ID
* Negative amount
* Zero amount
* Withdrawal exceeding available balance
* Invalid transfer source
* Invalid transfer target
* Invalid reversal request

Expected behavior:

```text
Handled business error
        ↓
Clear error message
        ↓
Program continues
```

The program must not terminate with an unhandled traceback for expected invalid operations.

---

## 11. Week 2 Project Files

The Week 2 implementation contains the following primary files:

```text
WEEK - 2/
│
├── README.md
├── TESTING.md
│
├── account.py
├── bank.py
├── main.py
├── transaction.py
├── storage_manager.py
│
├── test_bank.py
├── test_edge_cases.py
├── test_persistence.py
└── test_storage.py
```

### File Responsibilities

| File                  | Responsibility                                           |
| --------------------- | -------------------------------------------------------- |
| `account.py`          | Account data model and account-level behavior            |
| `bank.py`             | Core banking operations and business logic               |
| `transaction.py`      | Transaction representation                               |
| `main.py`             | Console application entry point                          |
| `storage_manager.py`  | Storage-related functionality used by the implementation |
| `test_bank.py`        | Core banking behavior tests                              |
| `test_edge_cases.py`  | Invalid and boundary-condition tests                     |
| `test_persistence.py` | Persistence-related verification                         |
| `test_storage.py`     | Storage behavior tests                                   |
| `TESTING.md`          | Testing documentation                                    |
| `README.md`           | Week 2 documentation                                     |

---

## 12. Testing

The Week 2 implementation includes automated tests covering:

* Account creation
* Deposits
* Withdrawals
* Transfers
* Transfer failure behavior
* Transaction history
* Transaction reversal
* Customer indexing
* Edge cases
* Storage-related behavior

Run the complete Week 2 test suite from this directory:

```powershell
python -m pytest -q
```

Expected result for the current implementation:

```text
14 passed
```

For detailed test names and individual results:

```powershell
python -m pytest -vv
```

---

## 13. Week 2 Acceptance Criteria

Week 2 is considered successfully implemented when all of the following are satisfied:

* [x] Money can be transferred between two accounts.
* [x] Total system balance remains unchanged after a successful transfer.
* [x] A failed transfer does not partially debit the sender.
* [x] Transfer failure is handled without an unhandled traceback.
* [x] Transactions are recorded.
* [x] The latest transaction can be reversed.
* [x] Exactly one transaction is reversed at a time.
* [x] Multiple accounts can belong to the same customer.
* [x] Customer-name indexing uses a secondary index.
* [x] Customer lookup returns all matching account IDs.
* [x] Invalid account operations are handled safely.
* [x] Invalid transaction amounts are rejected.
* [x] Automated tests pass successfully.

---

## 14. Required Week 2 Demonstrations

### Demonstration 1 — Successful Transfer

Create two accounts and transfer:

```text
₹1,000
```

Verify that:

```text
Sender balance decreases by ₹1,000
Receiver balance increases by ₹1,000
Total system balance remains unchanged
```

---

### Demonstration 2 — Failed Transfer

Attempt to transfer money to a non-existent account.

Before:

```text
Sender balance = X
```

Attempt:

```text
Transfer ₹1,000 → invalid account
```

After:

```text
Sender balance = X
```

The sender's balance must remain exactly unchanged.

---

### Demonstration 3 — Customer Index

Create two accounts for the same customer.

Perform one customer-index lookup.

Expected result:

```text
Both account IDs are returned.
```

---

### Demonstration 4 — Reversal

Perform a transaction and then call:

```text
reverse_last_transaction(account_id)
```

Verify that exactly the latest transaction is undone.

---

## 15. Week 2 Viva Question

### Question

> Transfer money to an account ID that does not exist. Prove that the sender's balance is exactly what it was before you tried.

### Expected Explanation

The transfer operation validates the required accounts and performs the operation atomically. If the target account is invalid or the second stage fails, the implementation rolls back the already-applied changes using the saved original state.

Therefore, a failed transfer does not leave a partial debit in the sender's account.

The important invariant is:

```text
Sender balance before failed transfer
=
Sender balance after failed transfer
```

---

## 16. Common Failure Modes Avoided

### Partial Transfer

Incorrect:

```text
Withdraw from sender
→ target validation fails
→ sender remains debited
```

Correct:

```text
Validate / perform atomically
→ rollback on failure
→ balances restored
```

---

### Missing Customer Index Update

Incorrect:

```text
Create account
→ forget to update customer index
```

Correct:

```text
Create account
→ add account ID to customer index
```

---

### Invalid Amounts

The implementation must not allow:

```text
₹0
negative amounts
```

for operations where a positive transaction amount is required.

---

### Unsafe Account Lookup

Account access must not blindly assume that an ID exists.

Invalid account IDs must be detected and handled explicitly.

---

## 17. Verification Status

Current Week 2 verification:

```text
Automated tests: 14 passed
Status: PASS
```

The Week 2 implementation has been verified against the core transfer, reversal, indexing, and edge-case requirements.

---

## 18. Relationship to the Overall Project

Week 2 is the second stage of the SecureBank development progression.

```text
Week 1
Account Fundamentals
       ↓
Week 2
Transfers + Reversals + Customer Index
       ↓
Week 3
Sorted Statements + Range Queries
       ↓
Week 4
JSON Persistence + Repository Bridge
       ↓
Week 5+
FastAPI → Architecture → Database → Security
→ Testing → Documentation → Production
```

The Week 2 implementation therefore establishes the transaction behavior that later weeks will build upon.

---

## 19. Reference Documents

Primary technical reference:

```text
R2021_Sem5_Weekly_Python_Backend.pdf
```

Week covered:

```text
Week 2 — Transfers, Reversals & Multi-Key Customer Indexing
```

Academic / placement reference:

```text
R2021_Sem5_Placement_Planner_V1.2_28Jul2026.docx
```

The Python Backend mini-project is part of the Semester 5 Training & Placement academic program, with assessment and corresponding internal marks based on test performance.

---

## 20. Project Repository

GitHub:

```text
https://github.com/sivaneshk23/PYTHON-BACKEND-PROJECT
```

---

## 21. Author

**Sivanesh K**

Python Backend Development Project

Semester 5 — B.Tech Artificial Intelligence and Data Science

J.J. College of Engineering and Technology
