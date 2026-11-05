"""
Gmail Integration & Synchronization Service
"""
import uuid
from typing import List, Dict, Any
from datetime import datetime


class GmailService:
    def __init__(self):
        pass

    def sync_inbox(self, user_id: int = 1) -> List[Dict[str, Any]]:
        """Simulate syncing latest unread emails from Gmail IMAP/OAuth."""
        # Returns simulated mock messages when credentials not bound
        mock_inbound = [
            {
                "message_id": f"GMAIL_{uuid.uuid4().hex[:10].upper()}",
                "thread_id": f"TH_G_{uuid.uuid4().hex[:6].upper()}",
                "sender_name": "Satya Nadella",
                "sender_email": "satya@enterprise-partner.com",
                "recipient_email": "shivam@mailmind.ai",
                "subject": "Follow-up: Signed NDA for AI Email Platform",
                "body_text": "Hi Shivam,\n\nOur legal team has countersigned the mutual NDA. Please find attached the preliminary API integration guidelines.",
                "snippet": "Our legal team has countersigned the mutual NDA...",
                "priority": "High",
                "sentiment": "Positive"
            }
        ]
        return mock_inbound
