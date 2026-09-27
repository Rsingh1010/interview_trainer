"""
Verifies the dice_sum solver against independent brute-force enumeration.
Run directly: python tests/test_dice_sum.py
Or with pytest: pytest tests/test_dice_sum.py
"""
import sys
import os
from fractions import Fraction
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "question_engine"))
from dice_sum import solve_dice_question


def brute_force(n, k, sides=6):
    total = sides ** n
    count = sum(1 for o in product(range(1, sides + 1), repeat=n) if sum(o) >= k)
    return Fraction(count, total)


def test_matches_brute_force_small_n():
    for n in range(1, 5):
        for k in range(n, 6 * n + 2):
            exact = solve_dice_question(n, k)
            brute = brute_force(n, k)
            assert exact == brute, f"n={n} k={k}: exact={exact} brute={brute}"


def test_edge_case_k_equals_n():
    for n in [1, 3, 5, 8]:
        assert solve_dice_question(n, n) == Fraction(1, 1)


def test_edge_case_k_equals_max():
    for n in [1, 3, 5]:
        assert solve_dice_question(n, 6 * n) == Fraction(1, 6 ** n)


def test_edge_case_k_greater_than_max():
    for n in [1, 3, 5]:
        assert solve_dice_question(n, 6 * n + 1) == Fraction(0, 1)


def test_edge_case_k_zero_or_negative():
    assert solve_dice_question(5, 0) == Fraction(1, 1)
    assert solve_dice_question(5, -3) == Fraction(1, 1)


if __name__ == "__main__":
    test_matches_brute_force_small_n()
    test_edge_case_k_equals_n()
    test_edge_case_k_equals_max()
    test_edge_case_k_greater_than_max()
    test_edge_case_k_zero_or_negative()
    print("All dice_sum tests passed.")