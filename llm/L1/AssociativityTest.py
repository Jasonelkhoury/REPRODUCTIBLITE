#!/usr/bin/env python3
"""
Experimental test of the associativity of floating-point addition.

For random triples (x, y, z) of IEEE 754 double-precision numbers, compare
(x + y) + z with x + (y + z) using exact equality. Count equal and different
results, print a summary, and write the results to answer_associativity_llm.txt.
"""

import random
import sys
from fractions import Fraction

OUTPUT_FILE = "answer_associativity_llm.txt"
NUM_TESTS = 1_000
INTERVAL_LOW = 0
INTERVAL_HIGH = 1
SEED = 42


def random_float(rng: random.Random, low: float, high: float) -> float:
    """Return a uniformly distributed float in [low, high)."""
    return rng.uniform(low, high)


def is_associative(x: float, y: float, z: float) -> bool:
    """Return True if (x + y) + z == x + (y + z) under exact float equality."""
    return (x + y) + z == x + (y + z)


def run_experiment(num_tests: int, low: float, high: float, seed: int):
    """Run the associativity experiment and return the counts."""
    rng = random.Random(seed)
    equal_count = 0
    different_count = 0
    counterexample = None

    for _ in range(num_tests):
        x = random_float(rng, low, high)
        y = random_float(rng, low, high)
        z = random_float(rng, low, high)

        if is_associative(x, y, z):
            equal_count += 1
        else:
            different_count += 1
            if counterexample is None:
                counterexample = (x, y, z)

    return equal_count, different_count, counterexample


def describe_counterexample(x: float, y: float, z: float) -> str:
    """Format a counterexample with its exact values for inspection."""
    left = (x + y) + z
    right = x + (y + z)
    lines = [
        f"  x = {x!r}",
        f"  y = {y!r}",
        f"  z = {z!r}",
        f"  (x + y) + z = {left!r}",
        f"  x + (y + z) = {right!r}",
        f"  exact difference (Fraction) = {float(Fraction(left) - Fraction(right))!r}",
    ]
    return "\n".join(lines)


def main() -> int:
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Interval: [{INTERVAL_LOW}, {INTERVAL_HIGH})")
    print(f"Random seed: {SEED}")
    print(f"Running {NUM_TESTS:,} tests...")

    equal_count, different_count, counterexample = run_experiment(
        NUM_TESTS, INTERVAL_LOW, INTERVAL_HIGH, SEED
    )
    total = equal_count + different_count
    percentage_equal = 100.0 * equal_count / total

    report_lines = [
        "Floating-point associativity experiment",
        f"Python version: {sys.version.split()[0]}",
        f"Interval: [{INTERVAL_LOW}, {INTERVAL_HIGH})",
        f"Random seed: {SEED}",
        "",
        f"Total tests: {total:,}",
        f"Equal results: {equal_count:,}",
        f"Different results: {different_count:,}",
        f"Percentage equal: {percentage_equal:.4f}%",
    ]

    if counterexample is not None:
        report_lines += [
            "",
            "First counterexample found:",
            describe_counterexample(*counterexample),
        ]

    report = "\n".join(report_lines) + "\n"

    print()
    print(report, end="")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Results written to {OUTPUT_FILE}")

    return 0


if __name__ == "__main__":
    sys.exit(main())