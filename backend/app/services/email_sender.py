"""
Email Dispatcher & SMTP Sender Service
"""
import uuid
from typing import Dict, Any, Optional
from datetime import datetime


class EmailSender:
    def __init__(self):
        pass

    def send_email(
        self,
        recipient: str,
        subject: str,
        body_text: str,
        sender_email: str = "shivam@mailmind.ai",
        sender_name: str = "Shivam Shakya"
    ) -> Dict[str, Any]:
        """Dispatch email through mock/SMTP gateway and log receipt."""
        message_id = f"MSG_OUT_{uuid.uuid4().hex[:12].upper()}"
        sent_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # In live production with credentials, smtplib.SMTP_SSL or SendGrid would be invoked here.
        return {
            "status": "sent",
            "message_id": message_id,
            "recipient": recipient,
            "subject": subject,
            "body_snippet": body_text[:100],
            "sent_at": sent_timestamp
        }
