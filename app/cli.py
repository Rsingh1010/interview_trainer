import sys
import os
import time
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "question_engine"))
from dice_sum import generate_dice_question, solve_dice_question

from db import get_connection, log_attempt

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "interview_trainer.db")
TOLERANCE = 0.005  # accept answers within 0.5% of the exact probability


def run():
    conn = get_connection(DB_PATH)
    difficulty = "easy"

    print("Interview Trainer - dice sum probability")
    print("Enter your answer as a decimal (e.g. 0.42). Type 'quit' to stop.\n")

    while True:
        q = generate_dice_question(difficulty)
        exact = solve_dice_question(q["n"], q["k"])
        exact_float = float(exact)

        print(q["question"])
        start = time.time()
        raw = input("Your answer: ").strip()
        elapsed = time.time() - start

        if raw.lower() == "quit":
            break

        try:
            user_answer = float(Fraction(raw))
        except (ValueError, ZeroDivisionError):
            print("Not a number, skipping this one.\n")
            continue

        correct = abs(user_answer - exact_float) < TOLERANCE

        print("Correct!" if correct else f"Not quite. Exact answer: {exact_float:.4f}")
        print()

        log_attempt(
            conn,
            family=q["family"],
            difficulty=q["difficulty"],
            n=q["n"],
            k=q["k"],
            correct_answer=exact_float,
            user_answer=user_answer,
            correct=correct,
            time_taken=elapsed,
        )

    conn.close()
    print("Session saved. Bye.")


if __name__ == "__main__":
    run()