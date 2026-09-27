import sqlite3

def get_connection(db_path="interview_trainer.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            n INTEGER,
            k INTEGER,
            correct_answer REAL NOT NULL,
            user_answer REAL,
            correct INTEGER,
            time_taken REAL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def log_attempt(conn, family, difficulty, n, k, correct_answer, user_answer, correct, time_taken):
    conn.execute("""
        INSERT INTO attempts (family, difficulty, n, k, correct_answer, user_answer, correct, time_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (family, difficulty, n, k, correct_answer, user_answer, int(correct), time_taken))
    conn.commit()