import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "question_engine"))
from dice_sum import generate_dice_question, solve_dice_question
from coin_streak import generate_coin_streak_question, solve_coin_streak

from db import get_connection, log_attempt
from fractions import Fraction

from flask import Flask, render_template, request

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "interview_trainer.db")
TOLERANCE = 0.01


def make_question(difficulty="easy"):
    family = random.choice(["dice_sum", "coin_streak"])
    if family == "dice_sum":
        q = generate_dice_question(difficulty)
        exact = solve_dice_question(q["parameters"]["n"], q["parameters"]["k"])
    else:
        q = generate_coin_streak_question(difficulty)
        exact = solve_coin_streak(q["parameters"]["n"], q["parameters"]["k"])
    q["exact_answer"] = float(exact)
    return q


@app.route("/")
def index():
    q = make_question()
    return render_template(
        "index.html",
        question=q["question"],
        family=q["family"],
        n=q["parameters"]["n"],
        k=q["parameters"]["k"],
        exact_answer=q["exact_answer"],
        difficulty=q["difficulty"],
        start_time=time.time(),
        result=None,
    )


@app.route("/answer", methods=["POST"])
def answer():
    family = request.form["family"]
    difficulty = request.form["difficulty"]
    n = int(request.form["n"])
    k = int(request.form["k"])
    exact_answer = float(request.form["exact_answer"])
    start_time = float(request.form["start_time"])
    raw = request.form["user_answer"].strip()

    elapsed = time.time() - start_time

    try:
        user_answer = float(Fraction(raw))
        parse_error = False
    except (ValueError, ZeroDivisionError):
        user_answer = None
        parse_error = True

    if not parse_error:
        correct = abs(user_answer - exact_answer) < TOLERANCE
        conn = get_connection(DB_PATH)
        log_attempt(
            conn,
            family=family,
            difficulty=difficulty,
            n=n,
            k=k,
            correct_answer=exact_answer,
            user_answer=user_answer,
            correct=correct,
            time_taken=elapsed,
        )
        conn.close()
        result = "Correct!" if correct else f"Not quite. Exact answer: {exact_answer:.4f}"
    else:
        result = "Couldn't read that as a number or fraction — try again."

    q = make_question()
    return render_template(
        "index.html",
        question=q["question"],
        family=q["family"],
        n=q["parameters"]["n"],
        k=q["parameters"]["k"],
        exact_answer=q["exact_answer"],
        difficulty=q["difficulty"],
        start_time=time.time(),
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)