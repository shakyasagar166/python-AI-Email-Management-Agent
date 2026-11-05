"""
AI Agent Intelligence REST Routes
"""
import sqlite3
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_db
from app.repositories.email_repository import EmailRepository
from app.services.email_service import EmailService
from app.services.reply_generator import ReplyGeneratorService
from app.schemas.email_schema import AIReplyRequest, AIAnalysisResponse
from app.config.ai_config import SUPPORTED_TONES, AI_MODELS

ai_router = APIRouter(prefix="/api/ai", tags=["AI Agent Intelligence"])


@ai_router.get("/config")
def get_ai_settings():
    return {
        "supported_tones": SUPPORTED_TONES,
        "available_models": AI_MODELS,
        "active_provider": "local-agent",
        "providers": ["OpenAI", "Anthropic", "Google Gemini", "Local Heuristic Engine"],
        "supported_intents": [
            "Meeting Request",
            "Action Required",
            "Inquiry / Question",
            "Feedback & Review",
            "Informational Update",
            "Acknowledge and Resolve"
        ]
    }


@ai_router.post("/analyze-email/{email_id}", response_model=Dict[str, Any])
def analyze_email_deeply(email_id: int, db: sqlite3.Connection = Depends(get_db)):
    service = EmailService(EmailRepository(db))
    email = service.get_email(email_id)

    # Classify & Intent & Priority
    intent_res = service.intent_detector.detect_intent(email["subject"], email["body_text"])
    priority_res = service.priority_detector.evaluate_priority(email["subject"], email["body_text"], email["sender_email"])
    cls_res = service.classifier.classify_email(email["subject"], email["sender_name"], email["body_text"])
    summary_res = service.summarizer.generate_summary(email["subject"], email["sender_name"], email["body_text"])

    reply_service = ReplyGeneratorService()
    suggested_draft = reply_service.generate_email_reply(
        subject=email["subject"],
        sender_name=email["sender_name"],
        body_text=email["body_text"],
        tone="Professional",
        intent=intent_res["intent"]
    )

    return {
        "email_id": email_id,
        "intent": intent_res["intent"],
        "priority": priority_res["priority"],
        "sentiment": priority_res["sentiment"],
        "category": cls_res["category"],
        "summary": summary_res,
        "suggested_reply": suggested_draft
    }


@ai_router.post("/generate-reply/{email_id}")
def generate_custom_reply(
    email_id: int,
    payload: AIReplyRequest,
    db: sqlite3.Connection = Depends(get_db)
):
    service = EmailService(EmailRepository(db))
    email = service.get_email(email_id)

    reply_service = ReplyGeneratorService()
    draft = reply_service.generate_email_reply(
        subject=email["subject"],
        sender_name=email["sender_name"],
        body_text=email["body_text"],
        tone=payload.tone or "Professional",
        intent=payload.intent or "Acknowledge and Resolve",
        custom_instructions=payload.custom_instructions or ""
    )

    # Save draft into database
    draft_id = EmailRepository(db).create_draft({
        "email_id": email_id,
        "user_id": 1,
        "reply_subject": draft["reply_subject"],
        "reply_body": draft["reply_body"],
        "tone": draft.get("tone", payload.tone),
        "intent": payload.intent or "Acknowledge and Resolve",
        "status": "Draft"
    })
    draft["draft_id"] = draft_id
    return draft
