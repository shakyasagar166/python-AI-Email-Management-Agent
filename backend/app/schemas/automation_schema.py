"""
Pydantic Schemas for Automation Rules
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel


class AutomationRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    condition_field: str  # sender, subject, category, priority, keyword
    condition_operator: str  # contains, equals, starts_with, regex
    condition_value: str
    action_type: str  # auto_reply, auto_archive, assign_category, mark_urgent, forward
    action_payload: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = True


class AutomationRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    condition_field: Optional[str] = None
    condition_operator: Optional[str] = None
    condition_value: Optional[str] = None
    action_type: Optional[str] = None
    action_payload: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None


class AutomationRuleResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    condition_field: str
    condition_operator: str
    condition_value: str
    action_type: str
    action_payload: Dict[str, Any]
    is_enabled: bool
    execution_count: int
    created_at: Optional[str] = None
