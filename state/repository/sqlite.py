import json
import sqlite3
from pathlib import Path
from state.repository.base import StateRepository


class SQLiteRepository(StateRepository):

    def __init__(self, database_path="data/assistant.db"):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    summary TEXT NOT NULL DEFAULT '',
                    summary_boundary INTEGER NOT NULL DEFAULT 0
                )
                """
            )

            connection.execute(
                """
                INSERT OR IGNORE INTO metadata (id)
                VALUES (1)
                """
            )

    def save_messages(self, messages):
        with self._connect() as connection:
            connection.execute("DELETE FROM messages")

            connection.executemany(
                "INSERT INTO messages (message) VALUES (?)",
                [
                    (json.dumps(message),)
                    for message in messages
                ],
            )

    def load_messages(self):
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT message FROM messages ORDER BY id"
            ).fetchall()

        return [
            json.loads(row[0])
            for row in rows
        ]

    def save_metadata(self, summary, summary_boundary):

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE metadata
                SET summary = ?, summary_boundary = ?
                WHERE id = 1
                """,
                (summary, summary_boundary)
            )

    def load_metadata(self):
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT summary, summary_boundary
                FROM metadata
                WHERE id = 1
                """
            ).fetchone()

        if row is None:
            return "", 0

        return row[0], row[1]