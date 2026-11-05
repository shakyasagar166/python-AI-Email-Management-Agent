"""
Priority & Urgency Scoring Engine
"""
from typing import Dict, Any


class PriorityDetector:
    def __init__(self):
        pass

    def evaluate_priority(self, subject: str, body: str, sender_email: str) -> Dict[str, Any]:
        """Compute email urgency priority (Urgent, High, Medium, Low)."""
        text = f"{subject} {body}".lower()

        urgency_score = 0

        # Urgent triggers
        if any(w in text for w in ["urgent", "asap", "emergency", "immediate", "term sheet", "critical alert"]):
            urgency_score += 4
        if any(w in text for w in ["alert", "outage", "high priority", "escalation", "deadline", "sla"]):
            urgency_score += 3
        if any(w in text for w in ["invoice", "meeting", "reschedule", "demo", "proposal"]):
            urgency_score += 2
        if any(w in text for w in ["newsletter", "digest", "weekly edition", "unsubscribe"]):
            urgency_score -= 2

        # Priority determination
        if urgency_score >= 4:
            priority = "Urgent"
        elif urgency_score >= 2:
            priority = "High"
        elif urgency_score >= 0:
            priority = "Medium"
        else:
            priority = "Low"

        # Sentiment heuristics
        sentiment = "Neutral"
        if any(w in text for w in ["enthusiastic", "thrilled", "great", "wonderful", "delighted", "appreciate"]):
            sentiment = "Positive"
        elif any(w in text for w in ["disappointed", "error", "spike", "outage", "poor", "unacceptable", "delay"]):
            sentiment = "Negative"

        return {
            "priority": priority,
            "urgency_score": urgency_score,
            "sentiment": sentiment
        }
