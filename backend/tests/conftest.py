"""
Pytest Fixtures for MailMind AI Backend Test Suite
"""
import os
import sys
import pytest

# Ensure backend root is on sys.path
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from app.config.database import init_db, get_connection
from app.repositories.email_repository import EmailRepository
from app.repositories.automation_repository import AutomationRepository
from app.repositories.user_repository import UserRepository
from app.services.email_service import EmailService
from app.services.automation_service import AutomationService


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Ensure database schema and sample seed data are initialized."""
    init_db()
    yield


@pytest.fixture
def db_conn():
    """Yields a database connection."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def email_repo(db_conn):
    return EmailRepository(db_conn)


@pytest.fixture
def auto_repo(db_conn):
    return AutomationRepository(db_conn)


@pytest.fixture
def user_repo(db_conn):
    return UserRepository(db_conn)


@pytest.fixture
def email_service(email_repo, auto_repo):
    return EmailService(email_repo, auto_repo)


@pytest.fixture
def automation_service(auto_repo, email_repo):
    return AutomationService(auto_repo, email_repo)


@pytest.fixture
def sample_email_payload():
    return {
        "sender_name": "Test Client",
        "sender_email": "test.client@example.com",
        "recipient_email": "alex.morgan@company.io",
        "subject": "Urgent: Project Deadline Escalation",
        "body_text": "Hi Alex, we urgently need the updated project timeline by 3 PM today. Please confirm ASAP.",
        "priority": "Urgent"
    }
