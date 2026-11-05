"""
Email Management REST Routes
"""
import sqlite3
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status, HTTPException
from app.config.database import get_db
from app.repositories.email_repository import EmailRepository
from app.repositories.automation_repository import AutomationRepository
from app.services.email_service import EmailService
from app.schemas.email_schema import EmailCreateRequest, EmailResponse

email_router = APIRouter(prefix="/api/emails", tags=["Emails"])


def get_service(db: sqlite3.Connection = Depends(get_db)) -> EmailService:
    return EmailService(EmailRepository(db), AutomationRepository(db))


@email_router.get("", response_model=List[Dict[str, Any]])
def list_emails(
    category_id: Optional[int] = None,
    priority: Optional[str] = None,
    is_read: Optional[bool] = None,
    is_starred: Optional[bool] = None,
    is_archived: Optional[bool] = False,
    search: Optional[str] = None,
    service: EmailService = Depends(get_service)
):
    return service.list_emails(
        user_id=1,
        category_id=category_id,
        priority=priority,
        is_read=is_read,
        is_starred=is_starred,
        is_archived=is_archived,
        search=search
    )


@email_router.get("/categories", response_model=List[Dict[str, Any]])
def get_categories(service: EmailService = Depends(get_service)):
    return service.get_categories()


@email_router.get("/dashboard/stats", response_model=Dict[str, Any])
def get_dashboard_stats(service: EmailService = Depends(get_service)):
    return service.get_dashboard_metrics(user_id=1)


@email_router.get("/{email_id}", response_model=Dict[str, Any])
def get_email(email_id: int, service: EmailService = Depends(get_service)):
    return service.get_email(email_id)


@email_router.post("", status_code=status.HTTP_201_CREATED)
def receive_email(payload: EmailCreateRequest, service: EmailService = Depends(get_service)):
    created = service.ingest_new_email(payload.model_dump(), user_id=1)
    return created


@email_router.patch("/{email_id}/read")
def toggle_read(email_id: int, is_read: bool = True, service: EmailService = Depends(get_service)):
    return service.set_read(email_id, is_read)


@email_router.patch("/{email_id}/star")
def toggle_star(email_id: int, is_starred: bool = True, service: EmailService = Depends(get_service)):
    return service.set_starred(email_id, is_starred)


@email_router.patch("/{email_id}/archive")
def toggle_archive(email_id: int, is_archived: bool = True, service: EmailService = Depends(get_service)):
    return service.set_archived(email_id, is_archived)


@email_router.delete("/{email_id}")
def delete_email(email_id: int, service: EmailService = Depends(get_service)):
    service.delete_email(email_id)
    return {"status": "success", "message": f"Email #{email_id} permanently deleted"}
