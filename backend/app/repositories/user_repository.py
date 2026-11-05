"""
User Repository for Database Persistence
"""
import sqlite3
from typing import Optional, Dict, Any


class UserRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        return cur.fetchone()

    def create(self, data: Dict[str, Any]) -> int:
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO users (email, password_hash, full_name, avatar_url, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["email"].strip().lower(),
                data["password_hash"],
                data["full_name"].strip(),
                data.get("avatar_url"),
                data.get("role", "User"),
                1 if data.get("is_active", True) else 0
            )
        )
        self.db.commit()
        return cur.lastrowid
