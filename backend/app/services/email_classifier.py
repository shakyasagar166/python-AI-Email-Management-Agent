"""
AI Email Classification Service
"""
import json
from typing import Dict, Any, Optional
from app.ai.llm_client import LLMClient
from app.ai.prompt_templates import EMAIL_CLASSIFICATION_PROMPT


class EmailClassifier:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def classify_email(self, subject: str, sender_name: str, body_text: str) -> Dict[str, Any]:
        """Classify incoming email into category with confidence rating."""
        prompt = EMAIL_CLASSIFICATION_PROMPT.format(
            subject=subject,
            sender=sender_name,
            body=body_text[:1000]
        )

        res_str = self.llm.complete(prompt, system_prompt="You are a strict JSON email classification engine.")
        try:
            parsed = json.loads(res_str)
            return {
                "category": parsed.get("category", "Primary & Internal"),
                "confidence": float(parsed.get("confidence", 0.90)),
                "reasoning": parsed.get("reasoning", "")
            }
        except Exception:
            return {
                "category": "Primary & Internal",
                "confidence": 0.85,
                "reasoning": "Default heuristic categorization."
            }
