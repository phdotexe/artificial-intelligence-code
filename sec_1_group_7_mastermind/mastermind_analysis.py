import time
import tracemalloc
from typing import Callable, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from ai_recursive_mastermind import (
    # COLORS,
    # NUM_POSITIONS,
    choose_best_guess_recursive,
    generate_all_codes,
    # solve_mastermind,
)


def measure_time(func: Callable, *args, **kwargs) -> Tuple[any, float]:  # type: ignore
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time


def measure_space(func: Callable, *args, **kwargs) -> Tuple[any, int]:  # type: ignore
    tracemalloc.start()
    result = func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


def analyze_time_complexity(
    test_sizes: List[int] = None,  # type: ignore
    max_depth: int = 3,  # type: ignore
) -> List[Dict]:
    if test_sizes is None:
        test_sizes = [10, 50, 100, 200, 500]

    all_codes = generate_all_codes()
    results = []

    print("\n" + "=" * 60)
    print("TIME COMPLEXITY ANALYSIS")
    print("=" * 60)
    print(f"Max recursion depth: {max_depth}")
    print()

    for size in test_sizes:
        if size > len(all_codes):
            size = len(all_codes)

        test_codes = all_codes[:size]

        _, elapsed = measure_time(
            choose_best_guess_recursive, test_codes, all_codes, False, max_depth
        )

        result = {
            "input_size": size,
            "time_seconds": elapsed,
            "max_depth": max_depth,
        }
        results.append(result)

        print(f"N={size:4d} codes: {elapsed:.4f} seconds")

    print()
    print("Theoretical: O(C * B^D * N) where B≈14 branching factor")

    return results


def analyze_space_complexity(
    test_sizes: List[int] = None,  # type: ignore
    max_depth: int = 3,  # type: ignore
) -> List[Dict]:
    if test_sizes is None:
        test_sizes = [10, 50, 100, 200]

    all_codes = generate_all_codes()
    results = []

    print("\n" + "=" * 60)
    print("SPACE COMPLEXITY ANALYSIS")
    print("=" * 60)
    print(f"Max recursion depth: {max_depth}")
    print()

    for size in test_sizes:
        if size > len(all_codes):
            size = len(all_codes)

        test_codes = all_codes[:size]

        _, peak_memory = measure_space(
            choose_best_guess_recursive, test_codes, all_codes, False, max_depth
        )

        result = {
            "input_size": size,
            "peak_memory_kb": peak_memory / 1024,
            "max_depth": max_depth,
        }
        results.append(result)

        print(f"N={size:4d} codes: {peak_memory / 1024:.2f} KB peak memory")

    print()
    print("Theoretical: O(D * N + M) where M is memoization table size")

    return results


def plot_time_complexity():
    n = np.linspace(1, 100, 100)

    f_n3 = n**3
    f_n3 = f_n3 / f_n3[-1]

    plt.figure(figsize=(10, 6))
    plt.plot(n, f_n3, "b-", linewidth=2, label="O(n³)")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Operations (normalized)")
    plt.title("Time Complexity: O(n³)")
    plt.legend()
    plt.grid(True)
    plt.savefig("time_complexity.png")
    plt.show()


def plot_space_complexity():
    n = np.linspace(1, 100, 100)

    f_n2 = n**2
    f_n2 = f_n2 / f_n2[-1]

    plt.figure(figsize=(10, 6))
    plt.plot(n, f_n2, "r-", linewidth=2, label="O(n²)")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Memory (normalized)")
    plt.title("Space Complexity: O(n²)")
    plt.legend()
    plt.grid(True)
    plt.savefig("space_complexity.png")
    plt.show()


if __name__ == "__main__":
    print("=" * 60)
    print("MASTERMIND Recursive algorithm - COMPLEXITY ANALYSIS".title())
    print("=" * 60)

    analyze_time_complexity(test_sizes=[10, 25, 50, 100], max_depth=3)
    analyze_space_complexity(test_sizes=[10, 25, 50, 100], max_depth=3)

    print("\n" + "=" * 60)
    print("THEORETICAL GROWTH PLOTS")
    print("=" * 60)
    plot_time_complexity()
    plot_space_complexity()

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
