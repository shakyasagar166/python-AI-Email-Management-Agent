"""
Input Validators & API Helper Utilities
"""
import re
from typing import Dict, Any
from app.exceptions.custom_exceptions import ValidationException


def validate_email_address(email: str) -> str:
    """Validate email address format."""
    if not email or not isinstance(email, str):
        raise ValidationException("Email address is required.")
    email = email.strip().lower()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValidationException(f"Invalid email format: '{email}'.")
    return email


def validate_required_string(val: str, field_name: str, min_len: int = 1) -> str:
    """Validate non-empty string."""
    if not val or not isinstance(val, str) or len(val.strip()) < min_len:
        raise ValidationException(f"{field_name} is required and must be at least {min_len} characters.")
    return val.strip()


def validate_automation_condition(field: str, operator: str, value: str):
    """Validate automation rule condition parameters."""
    allowed_fields = ["sender", "subject", "category", "priority", "keyword"]
    if field not in allowed_fields:
        raise ValidationException(f"Condition field must be one of: {', '.join(allowed_fields)}")

    allowed_ops = ["contains", "equals", "starts_with", "regex"]
    if operator not in allowed_ops:
        raise ValidationException(f"Condition operator must be one of: {', '.join(allowed_ops)}")

    if not value or not value.strip():
        raise ValidationException("Condition value cannot be empty.")
