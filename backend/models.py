import sqlite3
from datetime import datetime, UTC
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data.db"

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
"""

CREATE_LETTERS = """
CREATE TABLE IF NOT EXISTS letters_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    letter TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    attempts INTEGER NOT NULL DEFAULT 0,
    last_played TEXT,
    UNIQUE(user_id, letter)
);
"""

CREATE_REWARDS = """
CREATE TABLE IF NOT EXISTS rewards (
    user_id INTEGER PRIMARY KEY,
    stars INTEGER NOT NULL DEFAULT 0,
    stickers TEXT DEFAULT '',
    badges TEXT DEFAULT ''
);
"""

DEFAULT_LETTERS = [chr(c) for c in range(ord('A'), ord('Z')+1)]


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = _get_conn()
    cur = conn.cursor()
    cur.executescript(CREATE_USERS)
    cur.executescript(CREATE_LETTERS)
    cur.executescript(CREATE_REWARDS)
    # ensure default user and rewards
    cur.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?,?)", (1, "Child"))
    cur.execute("INSERT OR IGNORE INTO rewards (user_id, stars, stickers, badges) VALUES (?,?,?,?)",
                (1, 0, '', ''))
    # ensure letters rows exist for user 1
    for letter in DEFAULT_LETTERS:
        cur.execute("INSERT OR IGNORE INTO letters_progress (user_id, letter, completed, attempts) VALUES (?,?,?,?)",
                    (1, letter, 0, 0))
    conn.commit()
    conn.close()

def reset_rewards(user_id=1):
    """Reset rewards to initial state (for testing)."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE rewards SET stars=0, stickers='', badges='' WHERE user_id=?", (user_id,))
    cur.execute("UPDATE letters_progress SET completed=0, attempts=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def get_letters(user_id=1):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT letter, completed, attempts, last_played FROM letters_progress WHERE user_id=? ORDER BY letter", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_letter_progress(letter, correct, user_id=1):
    conn = _get_conn()
    cur = conn.cursor()
    # increment attempts
    cur.execute("UPDATE letters_progress SET attempts = attempts + 1, last_played = ? WHERE user_id=? AND letter=?", (datetime.now(UTC).isoformat(), user_id, letter))
    if correct:
        cur.execute("UPDATE letters_progress SET completed = 1 WHERE user_id=? AND letter=?", (user_id, letter))
    conn.commit()
    # return current row
    cur.execute("SELECT letter, completed, attempts, last_played FROM letters_progress WHERE user_id=? AND letter=?", (user_id, letter))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_rewards(user_id=1):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT stars, stickers, badges FROM rewards WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"stars": 0, "stickers": "", "badges": ""}


def add_stars(amount, user_id=1):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE rewards SET stars = stars + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()


def add_sticker(sticker_code, user_id=1):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT stickers FROM rewards WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    stickers = (row[0] or '').split(',') if row else []
    if sticker_code not in stickers:
        stickers = [s for s in stickers if s]
        stickers.append(sticker_code)
        cur.execute("UPDATE rewards SET stickers=? WHERE user_id=?", (','.join(stickers), user_id))
    conn.commit()
    conn.close()


def set_badge(badge_code, user_id=1):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT badges FROM rewards WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    badges = (row[0] or '').split(',') if row else []
    if badge_code not in badges:
        badges = [b for b in badges if b]
        badges.append(badge_code)
        cur.execute("UPDATE rewards SET badges=? WHERE user_id=?", (','.join(badges), user_id))
    conn.commit()
    conn.close()
