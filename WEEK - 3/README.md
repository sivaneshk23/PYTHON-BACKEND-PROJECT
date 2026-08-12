# Week 3 — Sorted Statements & Range Queries

> SecureBank Python Backend — Week 3 implementation focused on ordered data structures, sorted account views, transaction statements, efficient range queries, and empirical performance comparison.

## 1. Week Overview

Week 3 introduces ordered data structures into the SecureBank backend.

The objective is to generate sorted account views and efficient transaction statements while understanding the practical difference between Python's list-based `bisect` approach and a genuine sorted mapping structure using `sortedcontainers.SortedDict`.

This week also introduces efficient range querying through `SortedDict.irange()` and empirical performance measurement using Python's `timeit` module.

The implementation must demonstrate the difference between locating an insertion position efficiently and actually inserting into a Python list, where existing elements may need to be shifted.

---

## 2. Week 3 Objectives

The objectives of Week 3 are to:

* Maintain account IDs in sorted order.
* Produce account listings sorted by account ID.
* Produce account listings sorted by balance.
* Maintain transaction history in chronological order.
* Generate transaction statements for a specified date range.
* Use `bisect.insort()` for sorted list insertion.
* Use `bisect_left()` and `bisect_right()` for ordered boundary searches.
* Use `sortedcontainers.SortedDict` for ordered key-value storage.
* Use `SortedDict.irange()` for efficient range retrieval.
* Avoid manual filtering loops for the required range-query logic.
* Measure insertion performance using `timeit`.
* Compare `bisect.insort()` and `SortedDict` as the collection grows.
* Correctly handle multiple transactions occurring at the same timestamp.

---

## 3. Official Week 3 Scope

### Topic

```text
bisect & SortedDict — Sorted Statements & Range Queries
```

### Category

```text
In-Memory · Sorted Structures
```

### Required Package-Level Learning Progression

```text
LPA: 4
```

### Estimated Time

```text
6–8 hours
```

---

## 4. Required Functionality

### 4.1 Sorted Account Listings

The system must support account listings ordered by:

1. Account ID
2. Account balance

Example account IDs:

```text
105
101
110
103
```

Expected ID ordering:

```text
101
103
105
110
```

Balance ordering must also be deterministic. When two accounts have the same balance, a deterministic secondary key such as account ID should be used.

---

## 5. `bisect` Implementation

Python's `bisect` module is used for maintaining ordered account IDs.

The implementation uses:

```python
from bisect import insort
```

and:

```python
insort(sorted_ids, account_id)
```

The following operations are also used where appropriate:

```python
bisect_left()
bisect_right()
```

### Important Complexity Note

`bisect` performs the search for an insertion position efficiently, but the actual insertion into a Python list may require shifting existing elements.

Therefore:

```text
Finding insertion position
        ↓
Binary search
        ↓
Efficient search

Actual list insertion
        ↓
Elements may need to shift
        ↓
O(n)
```

`bisect.insort()` must therefore **not** be incorrectly described as O(log n) end-to-end.

This distinction is an important Week 3 learning objective.

---

## 6. `SortedDict`

The project uses:

```python
from sortedcontainers import SortedDict
```

`SortedDict` provides an ordered mapping structure suitable for maintaining sorted transaction history and performing ordered range operations.

It is used for the transaction-history portion of the Week 3 implementation.

Conceptually:

```text
Account
   ↓
Transaction History
   ↓
SortedDict
   ↓
(timestamp, transaction_id)
   ↓
Transaction
```

---

## 7. Transaction Ordering

Each account's transaction history must remain chronologically ordered.

The transaction history uses a sorted key.

The primary ordering value is:

```text
timestamp
```

A transaction identifier is used as a tie-breaker when required:

```text
(timestamp, transaction_id)
```

### Why the Tie-Breaker Is Required

Consider two transactions:

```text
Transaction 1 → 10:30:00.123456
Transaction 2 → 10:30:00.123456
```

If timestamp alone were used as the `SortedDict` key:

```python
history[timestamp] = transaction
```

both transactions would have the same key.

The second insertion could therefore replace the first transaction.

Instead, the implementation uses:

```text
(timestamp, transaction_id)
```

For example:

```text
(10:30:00.123456, 101)
(10:30:00.123456, 102)
```

These are different keys, so both transactions can be retained.

---

## 8. Range Queries with `irange()`

The Week 3 implementation uses:

```python
SortedDict.irange()
```

for ordered range retrieval.

The official example is:

```text
IDs:
101
103
105
110
```

Range:

```text
100 → 108
```

Expected result:

```text
101
103
105
```

The range must be obtained using the ordered data structure rather than manually filtering all elements with a `for` or `while` loop.

---

## 9. Date-Range Statements

The final Week 3 statement functionality must support a request such as:

```text
Transactions between 1 January and 15 January
```

The intended implementation is:

```text
Transaction History
        ↓
SortedDict
        ↓
.irange()
        ↓
Requested date range
        ↓
Statement
```

The date-range selection must not be implemented as a manual filtering loop.

The purpose is to demonstrate why an ordered data structure is useful when range queries are required.

---

## 10. Example Date-Range Query

Suppose an account has:

```text
1 January  → Deposit ₹5,000
5 January  → Withdrawal ₹1,000
10 January → Deposit ₹2,000
20 January → Withdrawal ₹500
```

A statement request for:

```text
1 January → 15 January
```

should return only:

```text
1 January  → Deposit ₹5,000
5 January  → Withdrawal ₹1,000
10 January → Deposit ₹2,000
```

The 20 January transaction must not be included.

The final implementation must obtain this range through `SortedDict.irange()`.

---

## 11. Performance Benchmark

Week 3 requires an empirical comparison between:

```text
bisect.insort()
```

and:

```text
SortedDict
```

The benchmark uses Python's:

```python
timeit
```

module.

### Required Dataset Size

The benchmark must use:

```text
5,000 insertions
```

The goal is not merely to state the theoretical complexity.

The performance difference must be **measured**.

---

## 12. Benchmark Objective

The benchmark should demonstrate that as the collection grows:

```text
bisect.insort()
```

becomes increasingly affected by list element shifting, while:

```text
SortedDict
```

provides a more appropriate ordered data structure for repeated sorted insertion and range operations.

The benchmark results should report measured execution time rather than simply claiming that one implementation is faster.

---

## 13. No Manual Filtering Requirement

The required range-query implementation must not contain manual filtering logic such as:

```python
for transaction in transactions:
    if start <= transaction.timestamp <= end:
        ...
```

or:

```python
while ...:
    ...
```

for the actual date-range selection.

The intended approach is:

```text
SortedDict
      ↓
irange()
      ↓
requested range
```

This requirement exists to demonstrate actual use of the ordered data structure rather than merely using it as decoration.

---

## 14. Current Week 3 Files

The Week 3 directory contains the implementation and verification files for this stage.

Current structure:

```text
WEEK - 3/
│
├── README.md
├── statement_service.py
└── test_statement_service.py
```

Additional benchmark/documentation files will be added as the remaining Week 3 requirements are completed.

Expected final Week 3 structure will include the statement implementation and a benchmark report.

---

## 15. Testing Strategy

Week 3 testing verifies both the new sorted-data functionality and regression safety.

Run the Week 3 test suite from this directory:

```powershell
python -m pytest -q
```

For detailed test names:

```powershell
python -m pytest -vv
```

Syntax verification:

```powershell
python -m py_compile statement_service.py test_statement_service.py
```

The official range example can also be verified directly using:

```python
SortedDict.irange()
```

---

## 16. Week 3 Current Test Coverage

The current Week 3 test suite verifies:

### Account Ordering

* Account IDs remain sorted.
* Duplicate account IDs are not inserted twice.
* Account ID range boundaries work correctly.
* Account existence can be checked using ordered lookup.
* Account IDs can be removed.
* Accounts can be returned sorted by ID.
* Accounts can be returned sorted by balance.

### Transaction Ordering

* Transactions are sorted by timestamp.
* Same-timestamp transactions are preserved.
* Transaction ID acts as the tie-breaker.
* Transaction ranges can be retrieved through the sorted structure.

---

## 17. Regression Testing

Week 3 must not break the functionality established during Week 2.

Run the Week 2 tests:

```powershell
cd "..\WEEK - 2"
python -m pytest -q
```

Expected current result:

```text
14 passed
```

Return to Week 3:

```powershell
cd "..\WEEK - 3"
```

Then run:

```powershell
python -m pytest -q
```

All Week 3 tests must pass before Week 3 changes are considered safe to commit.

---

## 18. Acceptance Criteria

Week 3 is considered complete when all of the following requirements are satisfied:

* [ ] Accounts can be displayed sorted by ID.
* [ ] Accounts can be displayed sorted by balance.
* [ ] `bisect.insort()` is used for the required sorted-list functionality.
* [ ] `bisect_left()` and `bisect_right()` are used appropriately.
* [ ] `SortedDict` is used for ordered transaction history.
* [ ] Transaction history is maintained in sorted order.
* [ ] Date-range statements are generated using `SortedDict.irange()`.
* [ ] No manual `for`/`while` filtering loop is used for the required range-selection logic.
* [ ] Same-timestamp transactions are handled using a tie-breaker key.
* [ ] The official ID range example works correctly.
* [ ] A 5,000-insertion benchmark is implemented.
* [ ] `timeit` is used for the benchmark.
* [ ] The performance difference between `bisect.insort()` and `SortedDict` is measured.
* [ ] Week 3 tests pass.
* [ ] Week 2 regression tests continue to pass.
* [ ] Code is syntax-checked.
* [ ] Documentation accurately reflects the implemented functionality.

---

## 19. Common Traps

### Trap 1 — Incorrect Big-O Claim

Incorrect:

```text
bisect.insort() = O(log n)
```

This ignores the cost of shifting elements in the Python list.

The search is efficient, but the list insertion itself can be O(n).

---

### Trap 2 — Manual Range Filtering

Incorrect:

```python
[
    transaction
    for transaction in transactions
    if start <= transaction.timestamp <= end
]
```

For the required Week 3 range-query demonstration, this defeats the purpose of using `SortedDict.irange()`.

---

### Trap 3 — Timestamp Collision

Incorrect:

```python
history[timestamp] = transaction
```

Two transactions with the same timestamp can collide.

Correct approach:

```python
history[(timestamp, transaction_id)] = transaction
```

---

### Trap 4 — Using `SortedDict` Without Using Its Range Features

Simply storing transactions in a `SortedDict` is not sufficient.

The project must demonstrate:

```text
SortedDict
    ↓
irange()
    ↓
range query
```

---

### Trap 5 — Benchmarking Without Measurement

A statement such as:

```text
"SortedDict is faster."
```

is not a benchmark.

The project must measure the implementations using:

```python
timeit
```

with the required 5,000 insertions.

---

## 20. Week 3 Viva Question

### Question

> Two of your transactions happened in the same microsecond. What happened to the first one, and how do you fix it?

### Expected Answer

If the timestamp alone is used as the `SortedDict` key, both transactions have the same key and the second transaction can overwrite the first.

The problem is solved by using a unique tie-breaker together with the timestamp:

```text
(timestamp, transaction_id)
```

The timestamp maintains chronological ordering, while the transaction ID distinguishes transactions that occur at the same timestamp.

---

## 21. Official Week 3 Deliverable

The required end-of-week deliverable is:

```text
statement_service.py
```

containing:

* Sorted account views
* Date-range transaction statements

and:

```text
Short timeit benchmark report
```

demonstrating the measured performance difference between the relevant sorted-data approaches.

---

## 22. Development Status

Current status:

```text
Week 3 — In Progress
```

Completed so far:

```text
✓ Sorted account IDs using bisect
✓ bisect_left()
✓ bisect_right()
✓ Account ID range lookup
✓ Account sorting by ID
✓ Account sorting by balance
✓ SortedDict transaction history
✓ Timestamp ordering
✓ Timestamp + transaction ID tie-breaker
✓ Same-timestamp transaction preservation
✓ Sorted transaction key-range retrieval
✓ Week 3 automated tests
✓ Week 2 regression verification
```

Remaining Week 3 work:

```text
→ Complete the final date-range statement interface
→ Verify the required no-manual-filtering implementation
→ Build the 5,000-insertion timeit benchmark
→ Record benchmark results
→ Complete final Week 3 regression testing
→ Prepare the short benchmark report
→ Final Week 3 documentation verification
```

---

## 23. Development Sequence

Week 3 follows this implementation progression:

```text
Week 2 Transaction System
          ↓
Sorted Account IDs
          ↓
bisect
          ↓
SortedDict
          ↓
Sorted Transaction History
          ↓
Timestamp + Tie-Breaker
          ↓
irange()
          ↓
Date-Range Statement
          ↓
timeit Benchmark
          ↓
Week 3 Final Verification
```

---

## 24. Reference Documents

Primary technical reference:

```text
R2021_Sem5_Weekly_Python_Backend.pdf
```

Relevant section:

```text
Week 3 — bisect & SortedDict — Sorted Statements & Range Queries
```

Academic / placement reference:

```text
R2021_Sem5_Placement_Planner_V1.2_28Jul2026.docx
```

---

## 25. Project Repository

GitHub:

```text
https://github.com/sivaneshk23/PYTHON-BACKEND-PROJECT
```

---

## 26. Author

**Sivanesh K**

Python Backend Development Project

Semester 5 — B.Tech Artificial Intelligence and Data Science

J.J. College of Engineering and Technology
