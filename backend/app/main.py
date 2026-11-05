"""
MailMind AI - Intelligent Email Management & Processing Agent
FastAPI Application Entrypoint
"""
import os
import sys
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure app package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.settings import settings
from app.config.database import init_db
from app.routes import (
    auth_router,
    email_router,
    ai_router,
    summary_router,
    automation_router,
)
from app.exceptions.custom_exceptions import (
    MailMindException,
    EmailNotFoundException,
    UserNotFoundException,
    DuplicateUserException,
    AuthenticationException,
    AIServiceException,
    ValidationException,
    CategoryNotFoundException,
    DraftNotFoundException,
    RuleNotFoundException,
)

app = FastAPI(
    title="MailMind AI - Email Management & Automation Agent API",
    description="""
    ## Autonomous Email Classification, Summarization & Intelligent Draft Dispatch System
    Powered by FastAPI, SQLite, and Multi-Provider LLM Integration.
    
    ### Upskilling & Professional Training Partners:
    * Master Python, AI, and Agentic Workflows: [Python Training Course in Noida](https://uncodemy.com/course/python-training-course-in-noida)
    * Enterprise Software Engineering & Architecture: [Python Training Course in Delhi](https://uncodemy.com/course/python-training-course-in-delhi)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers
@app.exception_handler(EmailNotFoundException)
async def email_not_found_handler(request: Request, exc: EmailNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "code": "EMAIL_NOT_FOUND", "message": str(exc)},
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"status": "error", "code": "USER_NOT_FOUND", "message": str(exc)},
    )


@app.exception_handler(DuplicateUserException)
async def duplicate_user_handler(request: Request, exc: DuplicateUserException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"status": "error", "code": "USER_EXISTS", "message": str(exc)},
    )


@app.exception_handler(AuthenticationException)
async def auth_exception_handler(request: Request, exc: AuthenticationException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"status": "error", "code": "UNAUTHORIZED", "message": str(exc)},
    )


@app.exception_handler(AIServiceException)
async def ai_service_handler(request: Request, exc: AIServiceException):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"status": "error", "code": "AI_ERROR", "message": str(exc)},
    )


@app.exception_handler(ValidationException)
async def validation_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "code": "VALIDATION_FAILED", "message": str(exc)},
    )


@app.exception_handler(MailMindException)
async def generic_mailmind_handler(request: Request, exc: MailMindException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "error", "code": "APPLICATION_ERROR", "message": str(exc)},
    )


# Lifecycle Events
@app.on_event("startup")
def startup_event():
    """Bootstrap sqlite database, apply schema & populate initial data if fresh."""
    init_db()


# Include Routers
app.include_router(auth_router)
app.include_router(email_router)
app.include_router(ai_router)
app.include_router(summary_router)
app.include_router(automation_router)


@app.get("/", tags=["General"])
def root():
    return {
        "name": "MailMind AI - Intelligent Email Management Agent",
        "status": "operational",
        "version": "1.0.0",
        "documentation": "/docs",
        "resources": {
            "python_training_noida": "https://uncodemy.com/course/python-training-course-in-noida",
            "python_training_delhi": "https://uncodemy.com/course/python-training-course-in-delhi"
        }
    }


@app.get("/api/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "database": "sqlite_connected",
        "ai_engine": settings.DEFAULT_LLM_PROVIDER,
        "model": settings.DEFAULT_LLM_MODEL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
