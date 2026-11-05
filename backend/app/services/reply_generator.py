"""
AI Reply Generator Service
"""
from typing import Dict, Any, Optional
from app.ai.response_generator import ResponseGenerator


class ReplyGeneratorService:
    def __init__(self, generator: Optional[ResponseGenerator] = None):
        self.generator = generator or ResponseGenerator()

    def generate_email_reply(
        self,
        subject: str,
        sender_name: str,
        body_text: str,
        tone: str = "Professional",
        intent: str = "Acknowledge and Resolve",
        custom_instructions: str = ""
    ) -> Dict[str, Any]:
        """Produce AI drafted response."""
        return self.generator.generate_reply(
            subject=subject,
            sender_name=sender_name,
            body_text=body_text,
            tone=tone,
            intent=intent,
            custom_instructions=custom_instructions
        )
