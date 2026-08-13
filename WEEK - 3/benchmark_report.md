# Week 3 Benchmark Report

## SecureBank Python Backend

### `bisect.insort()` vs `SortedDict`

---

## 1. Objective

The objective of this benchmark is to experimentally compare the insertion performance of:

* Python's `bisect.insort()`
* `sortedcontainers.SortedDict`

using a workload of 5,000 sorted insertions.

The benchmark is part of Week 3 of the SecureBank Python Backend project and demonstrates the practical performance characteristics of ordered data structures.

The comparison is intended to complement the theoretical complexity analysis of the two approaches.

---

## 2. Benchmark Requirements

The benchmark follows the Week 3 requirements:

* 5,000 insertions per benchmark run.
* `timeit`-based timing.
* Comparison between `bisect.insort()` and `SortedDict`.
* Deterministic insertion order.
* Multiple timing repetitions.
* Reporting of measured execution time.
* Explanation of the observed performance difference.
* No fabricated benchmark values.

---

## 3. Benchmark Environment

The benchmark was executed on the development machine used for the SecureBank Python Backend project.

Python version:

```text
Python 3.14.6
```

Operating system:

```text
Windows
```

Benchmark parameters:

```text
Insertions per run: 5,000
Number of runs per timing measurement: 5
Repeat count: 3
Deterministic seed: 20260813
```

The benchmark uses a fixed random seed so that the insertion order remains reproducible.

---

## 4. Methodology

Two independent implementations perform the same logical workload.

### Method A — `bisect.insort()`

A standard Python list is maintained in sorted order.

Each value is inserted using:

```python
insort(values, value)
```

The insertion position is found using binary search.

However, the actual list insertion can require existing elements to be shifted.

Therefore, although the search is efficient, the overall insertion operation can be dominated by the cost of moving list elements.

---

### Method B — `SortedDict`

A `SortedDict` is created and values are inserted using:

```python
values[value] = value
```

The structure maintains sorted keys and is designed for ordered mapping operations.

`SortedDict` is also used by the Week 3 statement implementation for ordered transaction history and range queries.

---

## 5. Workload

Each benchmark run inserts exactly:

```text
5,000 values
```

The values are:

```text
0 through 4,999
```

The insertion order is shuffled using a deterministic random seed:

```text
20260813
```

This avoids using an already-sorted insertion sequence and provides a more representative insertion workload for comparing the two data structures.

---

## 6. Timing Procedure

The benchmark uses Python's `timeit.repeat()` function.

Configuration:

```text
number = 5
repeat = 3
```

Therefore, each reported best timing represents:

```text
5,000 insertions × 5 runs
=
25,000 insertions
```

The minimum timing from the three repetitions is reported.

This reduces the influence of temporary background system activity on the selected measurement.

---

## 7. Measured Results

The benchmark produced the following results.

### `bisect.insort()`

```text
Best time for 25,000 insertions:
0.004210 seconds
```

Average measured time per insertion:

```text
0.000000168404 seconds
```

---

### `SortedDict`

```text
Best time for 25,000 insertions:
0.031550 seconds
```

Average measured time per insertion:

```text
0.000001262004 seconds
```

---

## 8. Results Table

| Implementation    | Insertions | Best measured time | Average time per insertion |
| ----------------- | ---------: | -----------------: | -------------------------: |
| `bisect.insort()` |     25,000 |         0.004210 s |           0.000000168404 s |
| `SortedDict`      |     25,000 |         0.031550 s |           0.000001262004 s |

---

## 9. Observed Performance

For this particular 5,000-insertion benchmark, `bisect.insort()` was faster than `SortedDict`.

Measured times:

```text
bisect.insort() = 0.004210 s
SortedDict      = 0.031550 s
```

The measured `SortedDict` time was approximately 7.49 times the measured `bisect.insort()` time for this workload.

This result must not be interpreted as meaning that `bisect.insort()` is always faster.

The benchmark measures one particular workload and one particular execution environment.

---

## 10. Why the Result Is Not a Contradiction

The benchmark result does not contradict the theoretical complexity discussion.

`bisect.insort()` performs an efficient binary search to locate the insertion position, but insertion into a Python list can require shifting existing elements.

Therefore, the insertion portion can have O(n) behavior.

However, for a relatively small collection such as 5,000 elements, Python's built-in list implementation can be highly optimized and may perform very well in practice.

`SortedDict` introduces additional data-structure management overhead. For a relatively small workload, this overhead can make its measured runtime higher than a simple Python list plus `bisect.insort()`.

Therefore:

```text
Theoretical complexity
        ≠
Guaranteed winner for every small benchmark
```

The benchmark is useful because it demonstrates the difference between theoretical complexity and actual measured performance.

---

## 11. Why `SortedDict` Is Still Required

The purpose of `SortedDict` in Week 3 is not simply to obtain the fastest possible insertion time for 5,000 integers.

The project requires operations that benefit from an ordered mapping structure, particularly:

```text
Sorted transaction history
        ↓
Ordered keys
        ↓
Range queries
        ↓
SortedDict.irange()
```

The Week 3 statement implementation therefore uses `SortedDict` for transaction history and range retrieval.

This is an example of selecting a data structure based on the operations the application needs rather than selecting one solely because it wins a single microbenchmark.

---

## 12. Complexity Discussion

### `bisect.insort()`

The binary search portion is efficient for locating the insertion point.

However, Python list insertion may require shifting existing elements.

Therefore, the overall insertion cost can be dominated by:

```text
O(n)
```

list movement.

---

### `SortedDict`

`SortedDict` is designed for maintaining sorted mappings and supporting ordered operations.

It is particularly useful for this project because it provides ordered access and range operations such as:

```python
history.irange(...)
```

This makes it appropriate for transaction statements and date-range queries.

---

## 13. Relationship to the SecureBank Project

The benchmark supports the Week 3 implementation decisions.

The project uses:

```text
bisect
```

for maintaining sorted account IDs.

The project uses:

```text
SortedDict
```

for ordered transaction history.

The project uses:

```text
SortedDict.irange()
```

for date-range transaction statements.

Therefore, the benchmark is not an isolated experiment. It demonstrates why different ordered data structures are useful for different application requirements.

---

## 14. Important Limitation

This benchmark should not be interpreted as a universal performance ranking.

The measured result depends on:

* Python version
* Processor
* Operating system
* Background processes
* Collection size
* Insertion order
* Benchmark configuration
* Implementation details of the installed `sortedcontainers` version

A larger dataset or a different workload can produce different results.

The benchmark should therefore be treated as an empirical observation for the tested environment rather than a universal statement.

---

## 15. Conclusion

The 5,000-insertion benchmark successfully measured the performance of `bisect.insort()` and `SortedDict`.

For the tested workload:

```text
bisect.insort()
→ 0.004210 seconds
```

```text
SortedDict
→ 0.031550 seconds
```

`bisect.insort()` was faster in this particular benchmark.

However, this does not eliminate the value of `SortedDict`. The two approaches have different characteristics, and `SortedDict` provides ordered mapping functionality that is particularly useful for the SecureBank transaction statement requirements.

The benchmark therefore demonstrates an important backend engineering principle:

> Data structures should be selected according to the operations and access patterns required by the application, while performance assumptions should be validated with measurements.

---

## 16. Verification Status

```text
5,000-insertion benchmark: PASS
timeit measurement: PASS
bisect.insort() measurement: PASS
SortedDict measurement: PASS
Deterministic workload: PASS
Measured results recorded: PASS
Benchmark report: COMPLETE
```

---

## 17. Reference

Primary technical specification:

```text
R2021_Sem5_Weekly_Python_Backend.pdf
```

Relevant section:

```text
Week 3 — bisect & SortedDict — Sorted Statements & Range Queries
```

Project repository:

```text
https://github.com/sivaneshk23/PYTHON-BACKEND-PROJECT
```

---

## 18. Author

**Sivanesh K**

SecureBank Python Backend Project

Semester 5 — B.Tech Artificial Intelligence and Data Science

J.J. College of Engineering and Technology
