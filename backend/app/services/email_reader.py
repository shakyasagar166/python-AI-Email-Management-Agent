"""
Email Ingestion & Content Reader Service
"""
import uuid
from typing import Dict, Any
from app.utils.email_parser import clean_text_content, extract_email_snippet, parse_sender_header


class EmailReader:
    def __init__(self):
        pass

    def parse_inbound_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert inbound webhook or SMTP data into standardized email attributes."""
        sender_raw = data.get("sender") or data.get("sender_email") or ""
        parsed_sender = parse_sender_header(sender_raw)

        sender_name = data.get("sender_name") or parsed_sender["name"]
        sender_email = parsed_sender["email"] or data.get("sender_email", "")

        body_raw = data.get("body") or data.get("body_text") or ""
        clean_body = clean_text_content(body_raw)
        snippet = data.get("snippet") or extract_email_snippet(clean_body)

        return {
            "message_id": data.get("message_id") or f"MSG_{uuid.uuid4().hex[:12].upper()}",
            "thread_id": data.get("thread_id") or f"TH_{uuid.uuid4().hex[:8].upper()}",
            "sender_name": sender_name,
            "sender_email": sender_email,
            "recipient_email": data.get("recipient_email", "").strip().lower(),
            "subject": data.get("subject", "No Subject").strip(),
            "body_text": clean_body,
            "body_html": data.get("body_html"),
            "snippet": snippet
        }
