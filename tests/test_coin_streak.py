"""
Verifies the coin_streak solver against independent brute-force enumeration.
Run directly: python tests/test_coin_streak.py
Or with pytest: pytest tests/test_coin_streak.py
"""
import sys
import os
from fractions import Fraction
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "question_engine"))
from coin_streak import solve_coin_streak


def brute_force(n, k):
    total = 2 ** n
    count = 0
    for outcome in product([0, 1], repeat=n):
        run = 0
        found = False
        for flip in outcome:
            if flip == 1:
                run += 1
                if run >= k:
                    found = True
                    break
            else:
                run = 0
        if found:
            count += 1
    return Fraction(count, total)


def test_matches_brute_force_small_n():
    for n in range(1, 17):
        for k in range(1, n + 2):
            exact = solve_coin_streak(n, k)
            brute = brute_force(n, k)
            assert exact == brute, f"n={n} k={k}: exact={exact} brute={brute}"


def test_edge_case_k_zero_or_negative():
    assert solve_coin_streak(10, 0) == Fraction(1, 1)
    assert solve_coin_streak(10, -2) == Fraction(1, 1)


def test_edge_case_k_greater_than_n():
    assert solve_coin_streak(5, 6) == Fraction(0, 1)


def test_edge_case_k_equals_n():
    assert solve_coin_streak(5, 5) == Fraction(1, 32)


if __name__ == "__main__":
    test_matches_brute_force_small_n()
    test_edge_case_k_zero_or_negative()
    test_edge_case_k_greater_than_n()
    test_edge_case_k_equals_n()
    print("All coin_streak tests passed.")