import random
from itertools import product
from fractions import Fraction


def generate_dice_question(difficulty="easy"):
    """
    Generate a random dice-sum probability question.

    Returns:
        dict: {family, difficulty, n, k, question}
    """

    if difficulty == "easy":
        n = random.randint(1, 3)
    elif difficulty == "medium":
        n = random.randint(2, 5)
    elif difficulty == "hard":
        n = random.randint(4, 8)
    else:
        raise ValueError("Difficulty must be easy, medium, or hard.")

    min_sum = n
    max_sum = 6 * n
    k = random.randint(min_sum, max_sum)

    return {
        "family": "dice_sum",
        "difficulty": difficulty,
        "parameters": {"n": n, "k": k},
        "question": f"You roll {n} fair six-sided dice. What is the probability that the sum is at least {k}?",
    }

def solve_dice_question(n, k):
    """
    Calculate the exact probability that the sum of n
    six-sided dice is at least k.

    Uses dynamic programming rather than simulation.

    Returns:
        Fraction: exact probability
    """
    if k <= 0:
        return Fraction(1, 1)

    # dp[s] = number of ways to get sum s
    dp = [0] * (6 * n + 1)
    dp[0] = 1

    for _ in range(n):
        new_dp = [0] * (6 * n + 1)

        for current_sum, count in enumerate(dp):
            if count == 0:
                continue

            for die_value in range(1, 7):
                new_dp[current_sum + die_value] += count

        dp = new_dp

    favorable_outcomes = sum(dp[k:])
    total_outcomes = 6 ** n

    return Fraction(favorable_outcomes, total_outcomes)

def brute_force_dice(n, k):
    """
    Independently calculate the probability by enumerating
    every possible dice outcome.

    Intended for small n because the number of outcomes is 6^n.

    Returns:
        Fraction: exact probability
    """

    total_outcomes = 0
    favorable_outcomes = 0

    for outcome in product(range(1, 7), repeat=n):
        total_outcomes += 1

        if sum(outcome) >= k:
            favorable_outcomes += 1

    return Fraction(favorable_outcomes, total_outcomes)


def verify_dice_solver(max_n=4):
    """
    Compare the exact solver against brute force for
    every possible threshold for n = 1 through max_n.
    """

    for n in range(1, max_n + 1):
        for k in range(n, 6 * n + 1):

            exact = solve_dice_question(n, k)
            brute_force = brute_force_dice(n, k)

            assert exact == brute_force, (
                f"Mismatch for n={n}, k={k}: "
                f"exact={exact}, brute_force={brute_force}"
            )

    print(f"All dice tests passed for n <= {max_n}.")


if __name__ == "__main__":
    verify_dice_solver()

    n, k = generate_dice_question("easy")

    answer = solve_dice_question(n, k)

    print(f"\nRoll {n} dice.")
    print(f"What is the probability that the sum is at least {k}?")
    print(f"Exact answer: {answer}")
    print(f"Decimal: {float(answer):.4f}")