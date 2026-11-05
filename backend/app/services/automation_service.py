"""
Agentic Automation Rules Engine Service
"""
import re
from typing import List, Dict, Any, Optional
from app.repositories.automation_repository import AutomationRepository
from app.repositories.email_repository import EmailRepository
from app.services.email_sender import EmailSender


class AutomationService:
    def __init__(
        self,
        rule_repo: AutomationRepository,
        email_repo: EmailRepository,
        sender: Optional[EmailSender] = None
    ):
        self.rule_repo = rule_repo
        self.email_repo = email_repo
        self.sender = sender or EmailSender()

    def evaluate_rules_for_email(self, email_data: Dict[str, Any], user_id: int = 1) -> List[Dict[str, Any]]:
        """Run all active rules against an incoming or existing email."""
        rules = self.rule_repo.get_all(user_id=user_id, enabled_only=True)
        triggered_actions = []

        for rule in rules:
            if self._matches_condition(rule, email_data):
                action_result = self._execute_action(rule, email_data)
                self.rule_repo.increment_execution(rule["id"])
                triggered_actions.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "action_type": rule["action_type"],
                    "result": action_result
                })

        return triggered_actions

    def _matches_condition(self, rule: Dict[str, Any], email: Dict[str, Any]) -> bool:
        field = rule["condition_field"].lower()
        operator = rule["condition_operator"].lower()
        target_val = rule["condition_value"].lower().strip()

        # Extract field value from email
        if field == "sender":
            actual_val = f"{email.get('sender_name', '')} {email.get('sender_email', '')}".lower()
        elif field == "subject":
            actual_val = email.get("subject", "").lower()
        elif field == "category":
            actual_val = str(email.get("category_name", "")).lower()
        elif field == "priority":
            actual_val = str(email.get("priority", "")).lower()
        elif field == "keyword":
            actual_val = f"{email.get('subject', '')} {email.get('body_text', '')}".lower()
        else:
            actual_val = ""

        if operator == "contains":
            return target_val in actual_val
        elif operator == "equals":
            return target_val == actual_val.strip()
        elif operator == "starts_with":
            return actual_val.startswith(target_val)
        elif operator == "regex":
            try:
                return bool(re.search(target_val, actual_val))
            except Exception:
                return False
        return False

    def _execute_action(self, rule: Dict[str, Any], email: Dict[str, Any]) -> Dict[str, Any]:
        action = rule["action_type"].lower()
        payload = rule.get("action_payload", {})
        email_id = email.get("id")

        if action == "mark_urgent" and email_id:
            self.email_repo.update_classification(email_id, category_id=None, priority="Urgent")
            if payload.get("star"):
                self.email_repo.set_star_status(email_id, True)
            return {"action": "marked_urgent", "starred": payload.get("star", False)}

        elif action == "auto_archive" and email_id:
            self.email_repo.set_archive_status(email_id, True)
            return {"action": "archived"}

        elif action == "assign_category" and email_id:
            cat_id = payload.get("category_id")
            priority = payload.get("priority")
            self.email_repo.update_classification(email_id, category_id=cat_id, priority=priority)
            return {"action": "category_assigned", "category_id": cat_id, "priority": priority}

        elif action == "auto_reply":
            reply_text = payload.get("reply_template", "Thank you for reaching out. We have received your inquiry.")
            res = self.sender.send_email(
                recipient=email["sender_email"],
                subject=f"Re: {email['subject']}",
                body_text=reply_text
            )
            return {"action": "auto_reply_dispatched", "receipt": res}

        return {"action": "none"}
