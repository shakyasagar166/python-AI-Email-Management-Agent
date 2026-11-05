"""
Master Email Service Facade
"""
from typing import List, Dict, Optional, Any
from app.repositories.email_repository import EmailRepository
from app.repositories.automation_repository import AutomationRepository
from app.services.email_reader import EmailReader
from app.services.email_classifier import EmailClassifier
from app.services.email_summarizer import EmailSummarizer
from app.services.automation_service import AutomationService
from app.ai.priority_detector import PriorityDetector
from app.ai.intent_detector import IntentDetector
from app.exceptions.custom_exceptions import EmailNotFoundException


class EmailService:
    def __init__(
        self,
        email_repo: EmailRepository,
        automation_repo: Optional[AutomationRepository] = None
    ):
        self.repo = email_repo
        self.reader = EmailReader()
        self.classifier = EmailClassifier()
        self.summarizer = EmailSummarizer()
        self.priority_detector = PriorityDetector()
        self.intent_detector = IntentDetector()
        self.automation_service = (
            AutomationService(automation_repo, email_repo) if automation_repo else None
        )

    def list_emails(
        self,
        user_id: int = 1,
        category_id: Optional[int] = None,
        priority: Optional[str] = None,
        is_read: Optional[bool] = None,
        is_starred: Optional[bool] = None,
        is_archived: Optional[bool] = 0,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self.repo.get_all(
            user_id=user_id,
            category_id=category_id,
            priority=priority,
            is_read=is_read,
            is_starred=is_starred,
            is_archived=is_archived,
            search=search
        )

    def get_email(self, email_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        email = self.repo.get_by_id(email_id, user_id)
        if not email:
            raise EmailNotFoundException(f"Email with ID {email_id} was not found.")
        return email

    def ingest_new_email(self, raw_data: Dict[str, Any], user_id: int = 1) -> Dict[str, Any]:
        """Full pipeline: Ingestion -> Priority Scoring -> Classification -> AI Summary -> Automation."""
        # 1. Parse content
        parsed = self.reader.parse_inbound_payload(raw_data)
        parsed["user_id"] = user_id

        # 2. Evaluate Priority & Sentiment
        p_res = self.priority_detector.evaluate_priority(
            parsed["subject"],
            parsed["body_text"],
            parsed["sender_email"]
        )
        parsed["priority"] = raw_data.get("priority") or p_res["priority"]
        parsed["sentiment"] = p_res["sentiment"]

        # 3. AI Categorization (if category not explicitly passed)
        if not parsed.get("category_id"):
            cls_res = self.classifier.classify_email(
                parsed["subject"],
                parsed["sender_name"],
                parsed["body_text"]
            )
            # Map category name to category_id
            cats = self.repo.get_categories()
            matched_cat = next((c for c in cats if c["name"].lower() == cls_res["category"].lower()), None)
            parsed["category_id"] = matched_cat["id"] if matched_cat else 1

        # 4. Save email
        email_id = self.repo.create(parsed)
        parsed["id"] = email_id

        # 5. Generate AI Summary & Key Points
        summary = self.summarizer.generate_summary(
            parsed["subject"],
            parsed["sender_name"],
            parsed["body_text"]
        )
        summary["email_id"] = email_id
        self.repo.upsert_summary(summary)

        # 6. Trigger Automation Rules
        if self.automation_service:
            self.automation_service.evaluate_rules_for_email(parsed, user_id=user_id)

        return self.get_email(email_id, user_id)

    def set_read(self, email_id: int, is_read: bool = True) -> Dict[str, Any]:
        self.get_email(email_id)
        self.repo.set_read_status(email_id, is_read)
        return {"id": email_id, "is_read": is_read}

    def set_starred(self, email_id: int, is_starred: bool = True) -> Dict[str, Any]:
        self.get_email(email_id)
        self.repo.set_star_status(email_id, is_starred)
        return {"id": email_id, "is_starred": is_starred}

    def set_archived(self, email_id: int, is_archived: bool = True) -> Dict[str, Any]:
        self.get_email(email_id)
        self.repo.set_archive_status(email_id, is_archived)
        return {"id": email_id, "is_archived": is_archived}

    def delete_email(self, email_id: int) -> bool:
        self.get_email(email_id)
        return self.repo.delete(email_id)

    def get_categories(self) -> List[Dict[str, Any]]:
        return self.repo.get_categories()

    def get_dashboard_metrics(self, user_id: int = 1) -> Dict[str, Any]:
        return self.repo.get_dashboard_stats(user_id=user_id)
