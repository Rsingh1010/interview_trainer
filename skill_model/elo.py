"""
Elo-style skill model for the interview trainer.

One skill number per question family. Difficulty tiers have fixed
anchor ratings. After each attempt, skill moves toward what the
observed result implies, scaled by K.
"""

DIFFICULTY_RATING = {
    "easy": 1000,
    "medium": 1300,
    "hard": 1600,
}

DEFAULT_STARTING_SKILL = 1200
K = 32
SCALE = 400


def expected_score(skill, difficulty_rating):
    """
    Probability of success given current skill vs. a difficulty rating.
    Standard logistic Elo curve.
    """
    return 1 / (1 + 10 ** ((difficulty_rating - skill) / SCALE))


def update_skill(skill, difficulty_rating, actual, k=K):
    """
    actual: 1 if correct, 0 if incorrect.
    Returns the new skill value.
    """
    expected = expected_score(skill, difficulty_rating)
    return skill + k * (actual - expected)


def replay_attempts(attempts, starting_skill=DEFAULT_STARTING_SKILL, k=K):
    """
    attempts: list of (difficulty_str, correct_bool), in chronological order.
    Returns the list of skill values AFTER each attempt (same length as attempts),
    so you can see the trajectory, not just the final number.
    """
    skill = starting_skill
    trajectory = []
    for difficulty, correct in attempts:
        difficulty_rating = DIFFICULTY_RATING[difficulty]
        skill = update_skill(skill, difficulty_rating, int(correct), k=k)
        trajectory.append(skill)
    return trajectory