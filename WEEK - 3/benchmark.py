from bisect import insort
from timeit import repeat

from sortedcontainers import SortedDict
from sqlalchemy import values


INSERTION_COUNT = 5_000
NUMBER_OF_RUNS = 5
REPEAT_COUNT = 3
SEED = 20260813

def create_insertion_values() -> list[int]:
    """
    Create a deterministic insertion order.

    A fixed seed makes the benchmark reproducible while
    avoiding an already-sorted insertion sequence.
    """
    import random

    values = list(range(INSERTION_COUNT))

    generator = random.Random(SEED)
    generator.shuffle(values)

    return values

def benchmark_bisect() -> None:
    """
    Measure 5,000 sorted insertions using bisect.insort().
    """

    insertion_values = create_insertion_values()

    def run() -> None:
        values: list[int] = []

        for value in insertion_values:
            insort(values, value)
    timings = repeat(
        run,
        number=NUMBER_OF_RUNS,
        repeat=REPEAT_COUNT
    )

    best_time = min(timings)

    total_insertions = (
        INSERTION_COUNT * NUMBER_OF_RUNS
    )

    average_time_per_insertion = (
        best_time / total_insertions
    )

    print("bisect.insort()")
    print(
        f"Best time for {total_insertions:,} insertions: "
        f"{best_time:.6f} seconds"
    )
    print(
        f"Average time per insertion: "
        f"{average_time_per_insertion:.12f} seconds"
    )


def benchmark_sorted_dict() -> None:
    """
    Measure 5,000 sorted insertions using SortedDict.
    """

    insertion_values = create_insertion_values()

    def run() -> None:
        values = SortedDict()

        for value in insertion_values:
            values[value] = value

    timings = repeat(
        run,
        number=NUMBER_OF_RUNS,
        repeat=REPEAT_COUNT
    )

    best_time = min(timings)

    total_insertions = (
        INSERTION_COUNT * NUMBER_OF_RUNS
    )

    average_time_per_insertion = (
        best_time / total_insertions
    )

    print("SortedDict")
    print(
        f"Best time for {total_insertions:,} insertions: "
        f"{best_time:.6f} seconds"
    )
    print(
        f"Average time per insertion: "
        f"{average_time_per_insertion:.12f} seconds"
    )


def main() -> None:
    print("=" * 60)
    print("SecureBank Week 3 Insertion Benchmark")
    print("=" * 60)
    print(f"Insertions per run: {INSERTION_COUNT:,}")
    print(f"Number of runs: {NUMBER_OF_RUNS}")
    print(f"Repeat count: {REPEAT_COUNT}")
    print()

    benchmark_bisect()

    print()

    benchmark_sorted_dict()

    print("=" * 60)


if __name__ == "__main__":
    main()