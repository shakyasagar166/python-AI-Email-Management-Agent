"""
Email, Summary & Draft Repository
"""
import json
import sqlite3
from typing import List, Dict, Optional, Any


class EmailRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def get_all(
        self,
        user_id: int = 1,
        category_id: Optional[int] = None,
        priority: Optional[str] = None,
        is_read: Optional[bool] = None,
        is_starred: Optional[bool] = None,
        is_archived: Optional[bool] = 0,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                e.*,
                c.name AS category_name,
                c.color AS category_color,
                s.one_sentence_summary,
                s.key_points_json,
                s.action_items_json,
                s.sentiment_score
            FROM emails e
            LEFT JOIN email_categories c ON e.category_id = c.id
            LEFT JOIN email_summaries s ON e.id = s.email_id
            WHERE e.user_id = ?
        """
        params = [user_id]

        if is_archived is not None:
            query += " AND e.is_archived = ?"
            params.append(1 if is_archived else 0)

        if category_id:
            query += " AND e.category_id = ?"
            params.append(category_id)

        if priority:
            query += " AND LOWER(e.priority) = LOWER(?)"
            params.append(priority.strip())

        if is_read is not None:
            query += " AND e.is_read = ?"
            params.append(1 if is_read else 0)

        if is_starred is not None:
            query += " AND e.is_starred = ?"
            params.append(1 if is_starred else 0)

        if search:
            query += """ AND (
                LOWER(e.subject) LIKE ? OR
                LOWER(e.sender_name) LIKE ? OR
                LOWER(e.sender_email) LIKE ? OR
                LOWER(e.body_text) LIKE ?
            )"""
            term = f"%{search.strip().lower()}%"
            params.extend([term, term, term, term])

        query += " ORDER BY e.received_at DESC, e.id DESC"
        cur = self.db.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

        # Parse JSON fields in summary
        for r in rows:
            if r.get("one_sentence_summary"):
                try:
                    r["summary"] = {
                        "one_sentence_summary": r["one_sentence_summary"],
                        "key_points": json.loads(r.get("key_points_json") or "[]"),
                        "action_items": json.loads(r.get("action_items_json") or "[]"),
                        "sentiment_score": r.get("sentiment_score", 0.0)
                    }
                except Exception:
                    r["summary"] = None
            else:
                r["summary"] = None
        return rows

    def get_by_id(self, email_id: int, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        query = """
            SELECT 
                e.*,
                c.name AS category_name,
                c.color AS category_color,
                s.one_sentence_summary,
                s.key_points_json,
                s.action_items_json,
                s.sentiment_score
            FROM emails e
            LEFT JOIN email_categories c ON e.category_id = c.id
            LEFT JOIN email_summaries s ON e.id = s.email_id
            WHERE e.id = ?
        """
        params = [email_id]
        if user_id:
            query += " AND e.user_id = ?"
            params.append(user_id)

        cur = self.db.cursor()
        cur.execute(query, params)
        row = cur.fetchone()
        if row and row.get("one_sentence_summary"):
            try:
                row["summary"] = {
                    "one_sentence_summary": row["one_sentence_summary"],
                    "key_points": json.loads(row.get("key_points_json") or "[]"),
                    "action_items": json.loads(row.get("action_items_json") or "[]"),
                    "sentiment_score": row.get("sentiment_score", 0.0)
                }
            except Exception:
                row["summary"] = None
        elif row:
            row["summary"] = None
        return row

    def create(self, data: Dict[str, Any]) -> int:
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO emails (
                message_id, thread_id, user_id, sender_name, sender_email,
                recipient_email, subject, body_text, body_html, snippet,
                category_id, priority, sentiment, is_read, is_starred,
                is_archived, is_spam, received_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                data.get("message_id"),
                data.get("thread_id"),
                data.get("user_id", 1),
                data["sender_name"],
                data["sender_email"],
                data["recipient_email"],
                data["subject"],
                data["body_text"],
                data.get("body_html"),
                data.get("snippet", ""),
                data.get("category_id"),
                data.get("priority", "Medium"),
                data.get("sentiment", "Neutral"),
                1 if data.get("is_read") else 0,
                1 if data.get("is_starred") else 0,
                1 if data.get("is_archived") else 0,
                1 if data.get("is_spam") else 0,
            )
        )
        self.db.commit()
        return cur.lastrowid

    def update_classification(
        self,
        email_id: int,
        category_id: Optional[int],
        priority: Optional[str] = None,
        sentiment: Optional[str] = None
    ) -> bool:
        cur = self.db.cursor()
        updates = []
        params = []
        if category_id is not None:
            updates.append("category_id = ?")
            params.append(category_id)
        if priority is not None:
            updates.append("priority = ?")
            params.append(priority)
        if sentiment is not None:
            updates.append("sentiment = ?")
            params.append(sentiment)

        if not updates:
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(email_id)
        sql = f"UPDATE emails SET {', '.join(updates)} WHERE id = ?"
        cur.execute(sql, params)
        self.db.commit()
        return cur.rowcount > 0

    def set_read_status(self, email_id: int, is_read: bool) -> bool:
        cur = self.db.cursor()
        cur.execute("UPDATE emails SET is_read = ? WHERE id = ?", (1 if is_read else 0, email_id))
        self.db.commit()
        return cur.rowcount > 0

    def set_star_status(self, email_id: int, is_starred: bool) -> bool:
        cur = self.db.cursor()
        cur.execute("UPDATE emails SET is_starred = ? WHERE id = ?", (1 if is_starred else 0, email_id))
        self.db.commit()
        return cur.rowcount > 0

    def set_archive_status(self, email_id: int, is_archived: bool) -> bool:
        cur = self.db.cursor()
        cur.execute("UPDATE emails SET is_archived = ? WHERE id = ?", (1 if is_archived else 0, email_id))
        self.db.commit()
        return cur.rowcount > 0

    def delete(self, email_id: int) -> bool:
        cur = self.db.cursor()
        cur.execute("DELETE FROM emails WHERE id = ?", (email_id,))
        self.db.commit()
        return cur.rowcount > 0

    # ---------------- Categories ----------------
    def get_categories(self) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM email_categories ORDER BY id ASC")
        return cur.fetchall()

    def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM email_categories WHERE id = ?", (category_id,))
        return cur.fetchone()

    # ---------------- Summaries ----------------
    def upsert_summary(self, data: Dict[str, Any]) -> int:
        cur = self.db.cursor()
        kp = json.dumps(data.get("key_points", []))
        act = json.dumps(data.get("action_items", []))

        cur.execute(
            """
            INSERT INTO email_summaries (
                email_id, one_sentence_summary, key_points_json, action_items_json, sentiment_score
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(email_id) DO UPDATE SET
                one_sentence_summary = excluded.one_sentence_summary,
                key_points_json = excluded.key_points_json,
                action_items_json = excluded.action_items_json,
                sentiment_score = excluded.sentiment_score,
                generated_at = CURRENT_TIMESTAMP
            """,
            (
                data["email_id"],
                data["one_sentence_summary"],
                kp,
                act,
                data.get("sentiment_score", 0.0)
            )
        )
        self.db.commit()
        return cur.lastrowid

    # ---------------- Drafts ----------------
    def get_drafts_by_email(self, email_id: int) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM email_drafts WHERE email_id = ? ORDER BY id DESC", (email_id,))
        return cur.fetchall()

    def get_all_drafts(self, user_id: int = 1) -> List[Dict[str, Any]]:
        cur = self.db.cursor()
        cur.execute("""
            SELECT d.*, e.subject AS original_subject, e.sender_name, e.sender_email
            FROM email_drafts d
            JOIN emails e ON d.email_id = e.id
            WHERE d.user_id = ?
            ORDER BY d.id DESC
        """, (user_id,))
        return cur.fetchall()

    def create_draft(self, data: Dict[str, Any]) -> int:
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO email_drafts (
                email_id, user_id, reply_subject, reply_body, tone, intent, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["email_id"],
                data.get("user_id", 1),
                data["reply_subject"],
                data["reply_body"],
                data.get("tone", "Professional"),
                data.get("intent", "Acknowledge and Resolve"),
                data.get("status", "Draft")
            )
        )
        self.db.commit()
        return cur.lastrowid

    def update_draft(self, draft_id: int, data: Dict[str, Any]) -> bool:
        cur = self.db.cursor()
        cur.execute(
            """
            UPDATE email_drafts SET
                reply_subject = ?, reply_body = ?, tone = ?,
                intent = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                data["reply_subject"],
                data["reply_body"],
                data.get("tone", "Professional"),
                data.get("intent", "Acknowledge and Resolve"),
                data.get("status", "Draft"),
                draft_id
            )
        )
        self.db.commit()
        return cur.rowcount > 0

    def delete_draft(self, draft_id: int) -> bool:
        cur = self.db.cursor()
        cur.execute("DELETE FROM email_drafts WHERE id = ?", (draft_id,))
        self.db.commit()
        return cur.rowcount > 0

    # ---------------- Dashboard Analytics ----------------
    def get_dashboard_stats(self, user_id: int = 1) -> Dict[str, Any]:
        cur = self.db.cursor()
        cur.execute("""
            SELECT 
                COUNT(*) AS total_inbox,
                SUM(CASE WHEN is_read = 0 THEN 1 ELSE 0 END) AS unread_count,
                SUM(CASE WHEN is_starred = 1 THEN 1 ELSE 0 END) AS starred_count,
                SUM(CASE WHEN priority = 'Urgent' THEN 1 ELSE 0 END) AS urgent_count,
                SUM(CASE WHEN is_archived = 1 THEN 1 ELSE 0 END) AS archived_count
            FROM emails
            WHERE user_id = ?
        """, (user_id,))
        totals = cur.fetchone() or {}

        cur.execute("""
            SELECT c.name, c.color, COUNT(e.id) AS count
            FROM email_categories c
            LEFT JOIN emails e ON c.id = e.category_id AND e.user_id = ? AND e.is_archived = 0
            GROUP BY c.id
        """, (user_id,))
        category_breakdown = cur.fetchall()

        cur.execute("SELECT COUNT(*) AS draft_count FROM email_drafts WHERE user_id = ?", (user_id,))
        draft_count = (cur.fetchone() or {}).get("draft_count", 0)

        cur.execute("SELECT COUNT(*) AS active_rules FROM automation_rules WHERE user_id = ? AND is_enabled = 1", (user_id,))
        active_rules = (cur.fetchone() or {}).get("active_rules", 0)

        return {
            "metrics": totals,
            "category_breakdown": category_breakdown,
            "draft_count": draft_count,
            "active_rules": active_rules
        }
