"""
Summary and Email Drafts Route Blueprint
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.database import get_db_connection
from app.repositories.email_repository import EmailRepository
from app.services.email_summarizer import EmailSummarizer
from app.schemas.email_schema import EmailSummaryResponse, DraftCreateRequest, DraftResponse
from app.exceptions.custom_exceptions import EmailNotFoundException, DraftNotFoundException

router = APIRouter(prefix="/api", tags=["Summaries & Drafts"])


@router.get("/summaries/email/{email_id}", response_model=Dict[str, Any])
def get_summary_by_email(email_id: int):
    """Retrieve existing AI summary for an email."""
    conn = get_db_connection()
    try:
        repo = EmailRepository(conn)
        email = repo.get_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail=f"Email ID {email_id} not found.")

        if not email.get("summary"):
            # If not yet generated, generate it automatically
            summarizer = EmailSummarizer()
            summary_data = summarizer.generate_summary(
                subject=email["subject"],
                sender_name=email["sender_name"],
                body_text=email["body_text"]
            )
            summary_data["email_id"] = email_id
            repo.upsert_summary(summary_data)
            return {"status": "success", "summary": summary_data}

        return {"status": "success", "summary": email["summary"]}
    finally:
        conn.close()


@router.post("/summaries/generate/{email_id}", response_model=Dict[str, Any])
def generate_summary_for_email(email_id: int):
    """Force generate/refresh AI summary, sentiment, and action items."""
    conn = get_db_connection()
    try:
        repo = EmailRepository(conn)
        email = repo.get_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail=f"Email ID {email_id} not found.")

        summarizer = EmailSummarizer()
        summary_data = summarizer.generate_summary(
            subject=email["subject"],
            sender_name=email["sender_name"],
            body_text=email["body_text"]
        )
        summary_data["email_id"] = email_id
        repo.upsert_summary(summary_data)
        return {
            "status": "success",
            "message": "AI summary refreshed successfully.",
            "summary": summary_data
        }
    finally:
        conn.close()


@router.get("/drafts", response_model=List[Dict[str, Any]])
def list_drafts(user_id: int = 1):
    """Fetch all saved or AI-generated reply drafts."""
    conn = get_db_connection()
    try:
        repo = EmailRepository(conn)
        drafts = repo.get_all_drafts(user_id=user_id)
        return drafts
    finally:
        conn.close()


@router.post("/drafts", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_draft(req: DraftCreateRequest, user_id: int = 1):
    """Save a manual or AI-generated reply draft."""
    conn = get_db_connection()
    try:
        repo = EmailRepository(conn)
        email = repo.get_by_id(req.email_id)
        if not email:
            raise HTTPException(status_code=404, detail=f"Email ID {req.email_id} does not exist.")

        data = req.model_dump()
        data["user_id"] = user_id
        draft_id = repo.create_draft(data)
        return {
            "status": "success",
            "message": "Reply draft saved successfully.",
            "draft_id": draft_id,
            "data": data
        }
    finally:
        conn.close()


@router.put("/drafts/{draft_id}", response_model=Dict[str, Any])
def update_draft(draft_id: int, req: DraftCreateRequest):
    """Update draft subject, body, tone, or status."""
    conn = get_db_connection()
    try:
        repo = EmailRepository(conn)
        updated = repo.update_draft(draft_id, req.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail=f"Draft ID {draft_id} not found.")
        return {"status": "success", "message": f"Draft {draft_id} updated successfully."}
    finally:
        conn.close()


@router.delete("/drafts/{draft_id}", response_model=Dict[str, Any])
def delete_draft(draft_id: int):
    """Delete draft by ID."""
    conn = get_db_connection()
    try:
        repo = EmailRepository(conn)
        deleted = repo.delete_draft(draft_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Draft ID {draft_id} not found.")
        return {"status": "success", "message": f"Draft {draft_id} discarded."}
    finally:
        conn.close()
