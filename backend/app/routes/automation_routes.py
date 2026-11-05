"""
Automation Rules Routes Blueprint
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.database import get_db_connection
from app.repositories.automation_repository import AutomationRepository
from app.schemas.automation_schema import AutomationRuleCreate, AutomationRuleUpdate, AutomationRuleResponse
from app.exceptions.custom_exceptions import RuleNotFoundException

router = APIRouter(prefix="/api/automations", tags=["Automation Rules"])


@router.get("", response_model=List[AutomationRuleResponse])
def get_all_rules(user_id: int = 1, enabled_only: bool = False):
    """List all active automation workflow rules."""
    conn = get_db_connection()
    try:
        repo = AutomationRepository(conn)
        return repo.get_all(user_id=user_id, enabled_only=enabled_only)
    finally:
        conn.close()


@router.get("/{rule_id}", response_model=AutomationRuleResponse)
def get_rule_by_id(rule_id: int):
    """Get single rule details."""
    conn = get_db_connection()
    try:
        repo = AutomationRepository(conn)
        rule = repo.get_by_id(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found.")
        return rule
    finally:
        conn.close()


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_rule(req: AutomationRuleCreate, user_id: int = 1):
    """Create a new automation rule with triggers and actions."""
    conn = get_db_connection()
    try:
        repo = AutomationRepository(conn)
        rule_data = req.model_dump()
        rule_data["user_id"] = user_id
        rule_id = repo.create(rule_data)
        return {
            "status": "success",
            "message": "Automation rule created successfully.",
            "rule_id": rule_id
        }
    finally:
        conn.close()


@router.put("/{rule_id}", response_model=Dict[str, Any])
def update_rule(rule_id: int, req: AutomationRuleUpdate):
    """Update rule condition, criteria, action, or state."""
    conn = get_db_connection()
    try:
        repo = AutomationRepository(conn)
        existing = repo.get_by_id(rule_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found.")

        updated = repo.update(rule_id, req.model_dump(exclude_unset=True))
        return {
            "status": "success",
            "message": f"Automation rule {rule_id} updated.",
            "updated": updated
        }
    finally:
        conn.close()


@router.patch("/{rule_id}/toggle", response_model=Dict[str, Any])
def toggle_rule(rule_id: int):
    """Toggle rule active/paused state."""
    conn = get_db_connection()
    try:
        repo = AutomationRepository(conn)
        existing = repo.get_by_id(rule_id)
        if not existing:
            raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found.")

        new_status = not existing["is_enabled"]
        repo.update(rule_id, {"is_enabled": new_status})
        return {
            "status": "success",
            "message": f"Rule {rule_id} is now {'enabled' if new_status else 'disabled'}.",
            "is_enabled": new_status
        }
    finally:
        conn.close()


@router.delete("/{rule_id}", response_model=Dict[str, Any])
def delete_rule(rule_id: int):
    """Delete automation rule."""
    conn = get_db_connection()
    try:
        repo = AutomationRepository(conn)
        deleted = repo.delete(rule_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found.")
        return {"status": "success", "message": f"Rule {rule_id} deleted."}
    finally:
        conn.close()
