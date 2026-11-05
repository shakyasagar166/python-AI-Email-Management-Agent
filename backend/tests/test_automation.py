"""
Automation Engine & Workflow Unit Tests
"""
import pytest


def test_list_automations(auto_repo):
    rules = auto_repo.get_all()
    assert isinstance(rules, list)
    assert len(rules) >= 2
    first = rules[0]
    assert "name" in first
    assert "condition_field" in first
    assert "action_type" in first


def test_crud_automation_rule(auto_repo):
    # 1. Create rule
    new_rule = {
        "user_id": 1,
        "name": "Auto-archive Stripe invoices",
        "description": "Archive invoices from Stripe",
        "condition_field": "sender_email",
        "condition_operator": "contains",
        "condition_value": "stripe.com",
        "action_type": "auto_archive",
        "action_payload": {},
        "is_enabled": True
    }
    rule_id = auto_repo.create(new_rule)
    assert rule_id > 0

    # 2. Get rule
    rule = auto_repo.get_by_id(rule_id)
    assert rule is not None
    assert rule["name"] == new_rule["name"]
    assert rule["is_enabled"] == 1

    # 3. Update rule
    updated = auto_repo.update(rule_id, {
        "name": "Auto-archive Stripe receipts and invoices",
        "is_enabled": False
    })
    assert updated is True
    refreshed = auto_repo.get_by_id(rule_id)
    assert refreshed["name"] == "Auto-archive Stripe receipts and invoices"
    assert refreshed["is_enabled"] == 0

    # 4. Delete rule
    deleted = auto_repo.delete(rule_id)
    assert deleted is True
    assert auto_repo.get_by_id(rule_id) is None


def test_condition_matching_logic(automation_service):
    # Contains match
    rule_contains = {
        "condition_field": "subject",
        "condition_operator": "contains",
        "condition_value": "security"
    }
    assert automation_service._matches_condition(
        rule_contains,
        {"subject": "Critical Security Notice from AWS", "sender_email": "aws@amazon.com", "priority": "Medium"}
    ) is True
    assert automation_service._matches_condition(
        rule_contains,
        {"subject": "Weekly team lunch", "sender_email": "hr@corp.com", "priority": "Low"}
    ) is False

    # Equals match
    rule_equals = {
        "condition_field": "priority",
        "condition_operator": "equals",
        "condition_value": "Urgent"
    }
    assert automation_service._matches_condition(rule_equals, {"priority": "Urgent"}) is True
    assert automation_service._matches_condition(rule_equals, {"priority": "Low"}) is False

    # Starts with match
    rule_starts = {
        "condition_field": "subject",
        "condition_operator": "starts_with",
        "condition_value": "[ALERT]"
    }
    assert automation_service._matches_condition(rule_starts, {"subject": "[ALERT] High CPU"}) is True
    assert automation_service._matches_condition(rule_starts, {"subject": "Re: [ALERT] High CPU"}) is False


def test_evaluate_and_execute_rules(automation_service, email_repo):
    # Ingest email that matches alert rule
    email = {
        "id": 1,
        "sender_name": "Ops Bot",
        "sender_email": "alerts@monitoring.internal",
        "subject": "[ALERT] Production Latency Spike",
        "body_text": "P99 latency has breached 500ms threshold.",
        "priority": "Medium",
        "is_archived": 0,
        "is_read": 0,
        "user_id": 1
    }
    executed_actions = automation_service.evaluate_rules_for_email(email, user_id=1)
    assert isinstance(executed_actions, list)
