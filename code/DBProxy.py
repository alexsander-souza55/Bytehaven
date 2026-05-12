import os
import sqlite3
from datetime import datetime

_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "bytehaven.db")


class DBProxy:
    def __init__(self):
        self._conn = sqlite3.connect(_DB)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT,
                score     INTEGER,
                timestamp TEXT
            )
        """)
        self._conn.commit()

    def save(self, name, score):
        ts = datetime.now().strftime("%H:%M - %d/%m/%y")
        self._conn.execute(
            "INSERT INTO scores (name, score, timestamp) VALUES (?, ?, ?)",
            (name[:4].upper(), score, ts)
        )
        self._conn.commit()

    def top(self, n=10):
        cur = self._conn.execute(
            "SELECT name, score, timestamp FROM scores ORDER BY score DESC LIMIT ?",
            (n,)
        )
        return cur.fetchall()

    def close(self):
        self._conn.close()
