"""
Intent Detection Engine for Incoming Emails
"""
import re
from typing import Dict, Any


class IntentDetector:
    def __init__(self):
        pass

    def detect_intent(self, subject: str, body: str) -> Dict[str, Any]:
        """Classify primary operational intent from subject and body."""
        text = f"{subject} {body}".lower()

        if any(w in text for w in ["sync", "meeting", "call", "schedule", "reschedule", "calendar", "invite", "zoom"]):
            intent = "Schedule Meeting"
            confidence = 0.95
        elif any(w in text for w in ["alert", "critical", "incident", "outage", "threshold", "pagerduty"]):
            intent = "System Alert & Incident"
            confidence = 0.98
        elif any(w in text for w in ["invoice", "payment", "bill", "balance", "$", "receipt", "charge"]):
            intent = "Billing & Financial Transaction"
            confidence = 0.96
        elif any(w in text for w in ["uncodemy", "course", "training", "python", "batch", "workshop"]):
            intent = "Python Training & Career Inquiry"
            confidence = 0.97
        elif any(w in text for w in ["complaint", "unacceptable", "disappointed", "latency spike", "delay", "poor"]):
            intent = "Customer Escalation / Complaint"
            confidence = 0.92
        elif any(w in text for w in ["rfp", "partnership", "pricing", "enterprise edition", "demo", "proposal"]):
            intent = "Commercial Partnership & Inquiry"
            confidence = 0.94
        elif any(w in text for w in ["bug", "error", "issue", "crash", "help", "support", "ticket"]):
            intent = "Technical Support Request"
            confidence = 0.90
        else:
            intent = "General Information Exchange"
            confidence = 0.85

        return {
            "intent": intent,
            "confidence": confidence
        }
