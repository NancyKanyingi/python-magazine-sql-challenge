import sqlite3
from pathlib import Path

DB_FILE = "magazine.db"

def get_connection():
    """Return a sqlite3 connection to DB_FILE with row factory set to sqlite3.Row."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create tables authors, magazines, and articles with foreign key constraints."""
    schema_dir = Path(".")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT
            );
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                author_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
                FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
            );
            """
        )

        conn.commit()
    finally:
        conn.close()
