import contextlib
import sqlite3
import os
import logging
from typing import Generator

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "products.db")

logger = logging.getLogger("werkzeug")

@contextlib.contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a SQLite connection and always close it on exit."""
    
    conn = sqlite3.connect(DB_PATH)

    if os.environ.get("SQL_TRACE", "0") == "1":
        conn.set_trace_callback(lambda sql: logger.debug("SQL EXECUTED: %s", sql))

    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                brand       TEXT    NOT NULL,
                price       REAL    NOT NULL,
                is_in_stock INTEGER NOT NULL DEFAULT 1,
                rating      REAL
            )
        """)
        conn.commit()
