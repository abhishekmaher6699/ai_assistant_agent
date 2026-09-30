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