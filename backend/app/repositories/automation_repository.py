"""
Automation Rule Repository for Database Persistence
"""
import json
import sqlite3
from typing import List, Dict, Optional, Any


class AutomationRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def get_all(self, user_id: int = 1, enabled_only: bool = False) -> List[Dict[str, Any]]:
        query = "SELECT * FROM automation_rules WHERE user_id = ?"
        params = [user_id]
        if enabled_only:
            query += " AND is_enabled = 1"
        query += " ORDER BY id DESC"

        cur = self.db.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

        for r in rows:
            if r.get("action_payload_json"):
                try:
                    r["action_payload"] = json.loads(r["action_payload_json"])
                except Exception:
                    r["action_payload"] = {}
            else:
                r["action_payload"] = {}
        return rows

    def get_by_id(self, rule_id: int) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM automation_rules WHERE id = ?", (rule_id,))
        row = cur.fetchone()
        if row:
            try:
                row["action_payload"] = json.loads(row.get("action_payload_json") or "{}")
            except Exception:
                row["action_payload"] = {}
        return row

    def create(self, data: Dict[str, Any]) -> int:
        cur = self.db.cursor()
        payload_str = json.dumps(data.get("action_payload", {}))
        cur.execute(
            """
            INSERT INTO automation_rules (
                user_id, name, description, condition_field, condition_operator,
                condition_value, action_type, action_payload_json, is_enabled
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("user_id", 1),
                data["name"],
                data.get("description", ""),
                data["condition_field"],
                data["condition_operator"],
                data["condition_value"],
                data["action_type"],
                payload_str,
                1 if data.get("is_enabled", True) else 0
            )
        )
        self.db.commit()
        return cur.lastrowid

    def update(self, rule_id: int, data: Dict[str, Any]) -> bool:
        cur = self.db.cursor()
        updates = []
        params = []

        fields = ["name", "description", "condition_field", "condition_operator", "condition_value", "action_type"]
        for f in fields:
            if f in data and data[f] is not None:
                updates.append(f"{f} = ?")
                params.append(data[f])

        if "action_payload" in data and data["action_payload"] is not None:
            updates.append("action_payload_json = ?")
            params.append(json.dumps(data["action_payload"]))

        if "is_enabled" in data and data["is_enabled"] is not None:
            updates.append("is_enabled = ?")
            params.append(1 if data["is_enabled"] else 0)

        if not updates:
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(rule_id)
        sql = f"UPDATE automation_rules SET {', '.join(updates)} WHERE id = ?"
        cur.execute(sql, params)
        self.db.commit()
        return cur.rowcount > 0

    def delete(self, rule_id: int) -> bool:
        cur = self.db.cursor()
        cur.execute("DELETE FROM automation_rules WHERE id = ?", (rule_id,))
        self.db.commit()
        return cur.rowcount > 0

    def increment_execution(self, rule_id: int) -> bool:
        cur = self.db.cursor()
        cur.execute("UPDATE automation_rules SET execution_count = execution_count + 1 WHERE id = ?", (rule_id,))
        self.db.commit()
        return cur.rowcount > 0
