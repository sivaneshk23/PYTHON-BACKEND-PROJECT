from bisect import insort
from timeit import repeat

from sortedcontainers import SortedDict


INSERTION_SIZES = (
    500,
    1000,
    2500,
    5000,
    10000,
    25000,
)

NUMBER_OF_RUNS = 3
REPEAT_COUNT = 3


def create_insertion_values(size: int) -> list[int]:
    return list(range(size - 1, -1, -1))


def benchmark_bisect(
    insertion_values: list[int],
) -> float:
    def run() -> None:
        values: list[int] = []

        for value in insertion_values:
            insort(values, value)

    timings = repeat(
        run,
        number=NUMBER_OF_RUNS,
        repeat=REPEAT_COUNT,
    )

    return min(timings) / (
        len(insertion_values) * NUMBER_OF_RUNS
    )


def benchmark_sorted_dict(
    insertion_values: list[int],
) -> float:
    def run() -> None:
        values = SortedDict()

        for value in insertion_values:
            values[value] = value

    timings = repeat(
        run,
        number=NUMBER_OF_RUNS,
        repeat=REPEAT_COUNT,
    )

    return min(timings) / (
        len(insertion_values) * NUMBER_OF_RUNS
    )


def main() -> None:
    print("=" * 80)
    print("SecureBank Week 3 Scaling Benchmark")
    print("=" * 80)
    print("Insertion order: descending")
    print(f"Runs per measurement: {NUMBER_OF_RUNS}")
    print(f"Repeat count: {REPEAT_COUNT}")
    print()

    print(
        f"{'Size':>8} "
        f"{'bisect.insort':>18} "
        f"{'SortedDict':>18} "
        f"{'bisect / SortedDict':>22}"
    )

    print("-" * 80)

    for size in INSERTION_SIZES:
        insertion_values = create_insertion_values(size)

        bisect_per_insert = benchmark_bisect(
            insertion_values
        )

        sorted_dict_per_insert = benchmark_sorted_dict(
            insertion_values
        )

        ratio = (
            bisect_per_insert /
            sorted_dict_per_insert
        )

        print(
            f"{size:>8,} "
            f"{bisect_per_insert:>18.12f} "
            f"{sorted_dict_per_insert:>18.12f} "
            f"{ratio:>22.2f}x"
        )

    print("=" * 80)


if __name__ == "__main__":
    main()