"""
AI Email Summarizer & Insight Extraction Service
"""
import json
from typing import Dict, Any, Optional
from app.ai.llm_client import LLMClient
from app.ai.prompt_templates import EMAIL_SUMMARIZATION_PROMPT


class EmailSummarizer:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def generate_summary(self, subject: str, sender_name: str, body_text: str) -> Dict[str, Any]:
        """Extract executive takeaway, key bullet points, and action items."""
        prompt = EMAIL_SUMMARIZATION_PROMPT.format(
            subject=subject,
            sender=sender_name,
            body=body_text[:1200]
        )

        res_str = self.llm.complete(prompt, system_prompt="You are an executive summary extractor.")
        try:
            parsed = json.loads(res_str)
            return {
                "one_sentence_summary": parsed.get("one_sentence_summary", f"Email regarding {subject}."),
                "key_points": parsed.get("key_points", [f"Discussion: {subject}"]),
                "action_items": parsed.get("action_items", ["Review message details"]),
                "sentiment_score": float(parsed.get("sentiment_score", 0.5))
            }
        except Exception:
            return {
                "one_sentence_summary": f"Inbound message from {sender_name} regarding '{subject}'.",
                "key_points": [f"Subject: {subject}", "Follow-up required"],
                "action_items": ["Review email body and take necessary action"],
                "sentiment_score": 0.5
            }
