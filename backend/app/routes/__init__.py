"""
Routes Module Initializer
"""
from app.routes.auth_routes import auth_router
from app.routes.email_routes import email_router
from app.routes.ai_routes import ai_router
from app.routes.summary_routes import router as summary_router
from app.routes.automation_routes import router as automation_router

__all__ = [
    "auth_router",
    "email_router",
    "ai_router",
    "summary_router",
    "automation_router",
]
