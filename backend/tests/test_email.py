"""
Email Management & Repository Unit Tests
"""
import pytest
from app.exceptions.custom_exceptions import EmailNotFoundException


def test_list_emails(email_service):
    emails = email_service.list_emails()
    assert isinstance(emails, list)
    assert len(emails) >= 5
    first = emails[0]
    assert "subject" in first
    assert "sender_name" in first
    assert "priority" in first
    assert "sentiment" in first


def test_get_email_by_id(email_service):
    email = email_service.get_email(1)
    assert email is not None
    assert email["id"] == 1
    assert "subject" in email
    assert "body_text" in email


def test_get_email_not_found(email_service):
    with pytest.raises(EmailNotFoundException):
        email_service.get_email(99999)


def test_get_categories(email_repo):
    categories = email_repo.get_categories()
    assert isinstance(categories, list)
    assert len(categories) >= 5
    names = [c["name"] for c in categories]
    assert "Client Inquiry" in names
    assert "Billing & Invoices" in names


def test_get_dashboard_stats(email_repo):
    stats = email_repo.get_dashboard_stats()
    assert "metrics" in stats
    assert "category_breakdown" in stats
    assert "draft_count" in stats
    assert "active_rules" in stats
    assert stats["metrics"]["total_inbox"] >= 5


def test_inbound_email_processing_pipeline(email_service, sample_email_payload):
    created = email_service.ingest_new_email(sample_email_payload)
    assert "id" in created
    assert created["subject"] == sample_email_payload["subject"]
    assert created["priority"] in ["Urgent", "High"]
    assert created["category_id"] is not None

    # Retrieve from DB to verify persistence
    saved = email_service.get_email(created["id"])
    assert saved["subject"] == sample_email_payload["subject"]


def test_email_status_updates(email_repo):
    # Toggle read
    res_read = email_repo.set_read_status(1, True)
    assert res_read is True
    email = email_repo.get_by_id(1)
    assert email["is_read"] == 1

    # Toggle star
    res_star = email_repo.set_star_status(1, True)
    assert res_star is True
    email = email_repo.get_by_id(1)
    assert email["is_starred"] == 1

    # Toggle archive
    res_archive = email_repo.set_archive_status(1, True)
    assert res_archive is True
    email = email_repo.get_by_id(1)
    assert email["is_archived"] == 1

    # Restore archive status
    email_repo.set_archive_status(1, False)


def test_search_and_filter_emails(email_service):
    # Filter by priority
    urgent_emails = email_service.list_emails(priority="Urgent", is_archived=None)
    assert all(e["priority"].lower() == "urgent" for e in urgent_emails)

    # Search keyword
    results = email_service.list_emails(search="Urgent", is_archived=None)
    assert len(results) > 0
