import random
from itertools import product
from fractions import Fraction


def generate_coin_streak_question(difficulty="easy"):
    """
    Question: Flip a fair coin N times. What is the probability
    of getting a streak of at least K consecutive heads?
    """
    if difficulty == "easy":
        n = random.randint(5, 8)
        k = random.randint(2, 3)
    elif difficulty == "medium":
        n = random.randint(8, 12)
        k = random.randint(3, 4)
    elif difficulty == "hard":
        n = random.randint(12, 18)
        k = random.randint(4, 6)
    else:
        raise ValueError("Difficulty must be easy, medium, or hard.")

    # guard: k must be achievable within n flips at all
    k = min(k, n)

    return {
        "family": "coin_streak",
        "difficulty": difficulty,
        "parameters": {"n": n, "k": k},
        "question": f"You flip a fair coin {n} times. What is the probability that you get a streak of at least {k} consecutive heads?",
    }


def solve_coin_streak(n, k):
    """
    Exact probability of at least one run of k consecutive heads
    in n fair coin flips.

    DP over "no success yet" states:
    f[j] = number of length-i sequences with no run of k heads yet,
           where j = current trailing run of heads (0 <= j < k).

    Transition per flip:
      - Tails: any state j -> state 0
      - Heads: state j -> state j+1, UNLESS j+1 == k, in which case
               that sequence now HAS a run of k heads and is excluded
               from the "no success" bucket entirely.

    Answer = 1 - (sequences with no success) / 2^n
    """
    if k <= 0:
        return Fraction(1, 1)
    if k > n:
        return Fraction(0, 1)

    # f[j] for j = 0 .. k-1
    f = [0] * k
    f[0] = 1  # empty sequence: trailing head-run = 0

    for _ in range(n):
        new_f = [0] * k
        for j in range(k):
            count = f[j]
            if count == 0:
                continue
            # flip tails -> reset to state 0
            new_f[0] += count
            # flip heads -> state j+1, unless that equals k (success, drop it)
            if j + 1 < k:
                new_f[j + 1] += count
            # if j+1 == k: these sequences now have the streak, excluded
        f = new_f

    no_success = sum(f)
    total = 2 ** n
    return Fraction(total - no_success, total)


def brute_force_coin_streak(n, k):
    """
    Independent enumeration: check every sequence of n coin flips
    for a run of >= k consecutive heads.
    """
    total = 2 ** n
    count = 0
    for outcome in product([0, 1], repeat=n):  # 1 = heads, 0 = tails
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


def verify_coin_streak(max_n=16):
    failures = []
    for n in range(1, max_n + 1):
        for k in range(1, n + 2):  # include k = n+1 (impossible -> 0)
            exact = solve_coin_streak(n, k)
            brute = brute_force_coin_streak(n, k)
            if exact != brute:
                failures.append((n, k, exact, brute))
    if failures:
        for n, k, e, b in failures[:10]:
            print(f"MISMATCH n={n} k={k}: exact={e} brute={b}")
    else:
        print(f"All coin streak tests passed for n <= {max_n}.")
    return len(failures) == 0


if __name__ == "__main__":
    verify_coin_streak(max_n=18)

    # edge cases
    print("k=0:", solve_coin_streak(10, 0))       # should be 1
    print("k>n:", solve_coin_streak(5, 6))         # should be 0
    print("k=n:", solve_coin_streak(5, 5))         # only 1 sequence: HHHHH -> 1/32