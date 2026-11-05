"""
Database Connection & Initialization Manager
"""
import sqlite3
from pathlib import Path
from typing import Generator
from app.config.settings import settings


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_connection(db_path: str = None) -> sqlite3.Connection:
    target_path = db_path or settings.DATABASE_PATH
    conn = sqlite3.connect(target_path, check_same_thread=False, timeout=10.0)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


get_db_connection = get_connection


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI Dependency for database session management."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_path: str = None):
    """Execute schema.sql and seed sample_data.sql into the target database."""
    target_path = db_path or settings.DATABASE_PATH
    conn = sqlite3.connect(target_path, timeout=10.0)
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        schema_file = Path(settings.SCHEMA_PATH)
        sample_file = Path(settings.SAMPLE_DATA_PATH)

        if schema_file.exists():
            with open(schema_file, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()

        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM emails")
        count = cur.fetchone()[0]
        if count == 0 and sample_file.exists():
            with open(sample_file, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()
            print("[Info] Sample email dataset initialized successfully.")
    finally:
        conn.close()
