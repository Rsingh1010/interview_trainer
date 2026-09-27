"""
Validates the Elo skill model using simulated learners with known,
fixed true skill levels. There's no ground truth for a real person's
skill, so this is the only way to check the model actually works:
generate synthetic attempts from a known skill, then check the
estimate converges toward it.

Important: a SINGLE simulated run is noisy (Elo has real variance
at realistic attempt counts, especially with random, non-adaptive
difficulty selection). This test checks that the AVERAGE estimate
across many independent simulated runs is close to the true skill
(i.e. the model is unbiased), not that any single run is precise.

Run directly: python tests/test_elo_convergence.py
Or with pytest: pytest tests/test_elo_convergence.py
"""
import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skill_model"))
from elo import expected_score, replay_attempts, DIFFICULTY_RATING

N_SEEDS = 40
N_ATTEMPTS = 100
MAX_AVG_ERROR = 60  # points, on the ~400-point Elo scale


def simulate_learner(true_skill, n_attempts, seed):
    rng = random.Random(seed)
    attempts = []
    for _ in range(n_attempts):
        difficulty = rng.choice(["easy", "medium", "hard"])
        true_p = expected_score(true_skill, DIFFICULTY_RATING[difficulty])
        correct = rng.random() < true_p
        attempts.append((difficulty, correct))
    return attempts


def average_error_for_skill(true_skill):
    errors = []
    for seed in range(N_SEEDS):
        attempts = simulate_learner(true_skill, N_ATTEMPTS, seed)
        trajectory = replay_attempts(attempts)
        errors.append(trajectory[-1] - true_skill)
    return sum(errors) / len(errors)


def test_converges_near_starting_prior():
    avg_error = average_error_for_skill(1200)
    assert abs(avg_error) < 20, f"avg_error={avg_error}"


def test_converges_for_below_average_skill():
    avg_error = average_error_for_skill(900)
    assert abs(avg_error) < MAX_AVG_ERROR, f"avg_error={avg_error}"


def test_converges_for_above_average_skill():
    avg_error = average_error_for_skill(1500)
    assert abs(avg_error) < MAX_AVG_ERROR, f"avg_error={avg_error}"


def test_known_limitation_extreme_skill_is_harder():
    # Documents a real, known limitation rather than hiding it:
    # far from the anchors, expected-score saturates and each
    # attempt carries less signal, so bias is larger even at n=100.
    # This assert is loose on purpose -- it exists to catch a
    # REGRESSION (things getting much worse), not to claim precision.
    avg_error = average_error_for_skill(1800)
    assert abs(avg_error) < 250, f"avg_error={avg_error} (expected large but bounded bias here)"


if __name__ == "__main__":
    test_converges_near_starting_prior()
    test_converges_for_below_average_skill()
    test_converges_for_above_average_skill()
    test_known_limitation_extreme_skill_is_harder()
    print("All elo convergence tests passed.")