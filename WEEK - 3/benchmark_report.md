# Week 3 Benchmark Report

## SecureBank Python Backend

### bisect.insort() vs SortedDict

## 1. Objective

The objective of this benchmark is to measure and compare the insertion performance of Python's `bisect.insort()` and `sortedcontainers.SortedDict`.

The benchmark specifically examines how the two approaches behave as the number of inserted elements increases.

This experiment supports the Week 3 requirement to demonstrate the practical performance difference between list-based sorted insertion and an ordered mapping structure.

## 2. Benchmark Requirements

The benchmark follows the Week 3 requirements:

- Use `bisect.insort()`.
- Use `SortedDict`.
- Use Python's `timeit` module.
- Include the required 5,000-insertion workload.
- Measure performance rather than simply claiming a complexity difference.
- Examine behavior as the collection grows.
- Record actual results from the development environment.
- Avoid fabricated or manually adjusted benchmark values.

## 3. Benchmark Configuration

The benchmark uses the following configuration:

```text
Insertion sizes:
500
1,000
2,500
5,000
10,000
25,000

Insertion order:
Descending

Runs per measurement:
3

Repeat count:
3