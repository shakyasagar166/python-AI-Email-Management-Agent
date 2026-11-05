"""
AI Contextual Response Drafting Engine
"""
import json
from typing import Dict, Any, Optional
from app.ai.llm_client import LLMClient
from app.ai.prompt_templates import REPLY_GENERATION_PROMPT


class ResponseGenerator:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def generate_reply(
        self,
        subject: str,
        sender_name: str,
        body_text: str,
        tone: str = "Professional",
        intent: str = "Acknowledge and Resolve",
        custom_instructions: str = ""
    ) -> Dict[str, Any]:
        """Generate drafted email response tailored to tone, intent and custom rules."""
        prompt = REPLY_GENERATION_PROMPT.format(
            subject=subject,
            sender=sender_name,
            body=body_text[:1200],
            tone=tone,
            intent=intent,
            custom_instructions=custom_instructions or "None"
        )

        res_str = self.llm.complete(prompt, system_prompt="You are MailMind, an expert enterprise email executive.")
        try:
            parsed = json.loads(res_str)
            return parsed
        except Exception:
            # Fallback formatting
            return {
                "reply_subject": f"Re: {subject}",
                "reply_body": (
                    f"Hi {sender_name},\n\n"
                    f"Thank you for contacting us regarding '{subject}'.\n\n"
                    f"We have noted your comments and will follow up with actionable next steps shortly.\n\n"
                    f"Best regards,\nMailMind AI Team"
                ),
                "tone": tone,
                "confidence": 0.85
            }
