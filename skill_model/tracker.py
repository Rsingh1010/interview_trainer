"""
Computes current per-family skill estimates from logged attempts
in the SQLite database, using the Elo replay model.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from db import get_connection
from elo import replay_attempts, DEFAULT_STARTING_SKILL


def get_current_skill(db_path, family):
    """
    Reads all logged attempts for this family, in chronological order,
    and returns the current skill estimate after replaying them through Elo.
    Returns DEFAULT_STARTING_SKILL if there are no attempts yet.
    """
    conn = get_connection(db_path)  # creates the table if it doesn't exist yet
    rows = conn.execute(
        "SELECT difficulty, correct FROM attempts WHERE family = ? ORDER BY id ASC",
        (family,)
    ).fetchall()
    conn.close()

    if not rows:
        return DEFAULT_STARTING_SKILL

    attempts = [(difficulty, bool(correct)) for difficulty, correct in rows]
    trajectory = replay_attempts(attempts)
    return trajectory[-1]


def get_attempt_count(db_path, family):
    conn = get_connection(db_path)
    count = conn.execute(
        "SELECT COUNT(*) FROM attempts WHERE family = ?", (family,)
    ).fetchone()[0]
    conn.close()
    return count