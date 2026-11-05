from .user_schema import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from .email_schema import (
    EmailCreateRequest,
    EmailResponse,
    EmailSummaryResponse,
    DraftCreateRequest,
    DraftResponse,
    AIReplyRequest,
    AIAnalysisResponse
)
from .automation_schema import AutomationRuleCreate, AutomationRuleUpdate, AutomationRuleResponse

__all__ = [
    "UserRegisterRequest",
    "UserLoginRequest",
    "UserResponse",
    "TokenResponse",
    "EmailCreateRequest",
    "EmailResponse",
    "EmailSummaryResponse",
    "DraftCreateRequest",
    "DraftResponse",
    "AIReplyRequest",
    "AIAnalysisResponse",
    "AutomationRuleCreate",
    "AutomationRuleUpdate",
    "AutomationRuleResponse"
]
