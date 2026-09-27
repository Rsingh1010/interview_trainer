"""
Adaptive difficulty selection: given a current skill estimate,
pick the difficulty tier whose anchor rating is closest to skill.
This keeps expected success near 0.5, which is where each attempt
carries the most information about true skill.
"""
from elo import DIFFICULTY_RATING


def choose_difficulty(skill):
    """
    Returns the difficulty tier ('easy', 'medium', 'hard') whose
    anchor rating is closest to the given skill estimate.
    """
    closest = min(
        DIFFICULTY_RATING.items(),
        key=lambda item: abs(item[1] - skill)
    )
    return closest[0]