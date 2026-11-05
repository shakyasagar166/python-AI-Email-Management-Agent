"""
AI Agent Intelligence & Reasoning Tests
"""
import pytest
from app.ai.intent_detector import IntentDetector
from app.ai.priority_detector import PriorityDetector
from app.ai.response_generator import ResponseGenerator
from app.services.email_classifier import EmailClassifier
from app.services.email_summarizer import EmailSummarizer
from app.config.ai_config import SUPPORTED_TONES, AI_MODELS


def test_ai_config_constants():
    assert "Professional" in SUPPORTED_TONES
    assert "Formal" in SUPPORTED_TONES
    assert "Casual" in SUPPORTED_TONES
    assert len(AI_MODELS) >= 3


def test_intent_detector():
    detector = IntentDetector()

    # Meeting intent
    res_meet = detector.detect_intent(
        subject="Sync on Q3 goals",
        body="Can we schedule a quick call tomorrow at 2 PM to review the roadmap?"
    )
    assert res_meet["intent"] == "Schedule Meeting"
    assert res_meet["confidence"] > 0.8

    # Alert intent
    res_alert = detector.detect_intent(
        subject="CRITICAL: Outage on DB replica",
        body="Pagerduty incident triggered for production database."
    )
    assert res_alert["intent"] == "System Alert & Incident"

    # Billing intent
    res_bill = detector.detect_intent(
        subject="Invoice #4928 Payment Due",
        body="Please find attached bill for your monthly cloud subscription."
    )
    assert res_bill["intent"] == "Billing & Financial Transaction"


def test_priority_detector():
    detector = PriorityDetector()

    # Urgent email
    res_urgent = detector.evaluate_priority(
        subject="EMERGENCY: Production cluster down",
        body="Outage ongoing, critical severity. Immediate attention needed.",
        sender_email="alerts@pagerduty.com"
    )
    assert res_urgent["priority"] in ["Urgent", "High"]
    assert res_urgent["sentiment"] == "Negative"

    # Low priority newsletter
    res_low = detector.evaluate_priority(
        subject="Weekly digest: Top 10 Tech trends",
        body="Here is your regular weekly update. Unsubscribe anytime.",
        sender_email="newsletter@digest.io"
    )
    assert res_low["priority"] in ["Low", "Medium"]


def test_email_classifier():
    classifier = EmailClassifier()
    result = classifier.classify_email(
        subject="Invoice #48293 for Cloud Infrastructure",
        sender_name="Stripe Billing",
        body_text="Your monthly invoice for cloud compute services is attached."
    )
    assert "category" in result
    assert result["category"] in ["Billing & Invoices", "Invoices & Finance", "Work", "Notifications"]


def test_email_summarizer():
    summarizer = EmailSummarizer()
    res = summarizer.generate_summary(
        subject="Q3 Product Launch Readiness",
        sender_name="Sarah Product Lead",
        body_text="Hi Team, we have completed the final regression tests. The release is scheduled for Friday at 9am. Please ensure all staging environments are locked by Thursday evening."
    )
    assert "one_sentence_summary" in res
    assert len(res["one_sentence_summary"]) > 0
    assert isinstance(res["key_points"], list)
    assert isinstance(res["action_items"], list)
    assert len(res["action_items"]) > 0


def test_response_generator():
    generator = ResponseGenerator()
    reply = generator.generate_reply(
        subject="Contract proposal inquiry",
        sender_name="John Partner",
        body_text="Could you clarify the payment milestones?",
        tone="Professional"
    )
    assert isinstance(reply, dict)
    assert "reply_body" in reply
    assert len(reply["reply_body"]) > 30
    assert "reply_subject" in reply


def test_draft_repository_lifecycle(email_repo):
    # 1. Create draft
    draft_id = email_repo.create_draft({
        "email_id": 1,
        "user_id": 1,
        "reply_subject": "Re: Strategic API Partnership Term Sheet",
        "reply_body": "Thank you for the draft term sheet. We are reviewing Section 4.",
        "tone": "Formal",
        "intent": "Acknowledge and Resolve",
        "status": "Draft"
    })
    assert draft_id > 0

    # 2. Retrieve draft
    drafts = email_repo.get_all_drafts(user_id=1)
    matched = next((d for d in drafts if d["id"] == draft_id), None)
    assert matched is not None
    assert matched["reply_subject"] == "Re: Strategic API Partnership Term Sheet"

    # 3. Update draft
    updated = email_repo.update_draft(draft_id, {
        "reply_subject": "Re: Strategic API Partnership (Revised)",
        "reply_body": "Updated draft response content.",
        "tone": "Professional",
        "intent": "Acknowledge and Resolve",
        "status": "Ready to Send"
    })
    assert updated is True

    # 4. Delete draft
    deleted = email_repo.delete_draft(draft_id)
    assert deleted is True
