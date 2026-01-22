"""
Tests for redaction pattern detection
"""
import pytest
from app.services.redaction_patterns import RedactionPatterns


def test_find_emails():
    """Test email detection"""
    text = "Contact me at john.doe@example.com or jane@test.org"
    emails = RedactionPatterns.find_emails(text)
    assert len(emails) == 2
    assert "john.doe@example.com" in emails
    assert "jane@test.org" in emails


def test_find_phones():
    """Test phone number detection"""
    text = "Call me at (555) 123-4567 or 555-987-6543"
    phones = RedactionPatterns.find_phones(text)
    assert len(phones) >= 2


def test_find_linkedin():
    """Test LinkedIn URL detection"""
    text = "My profile: https://linkedin.com/in/johndoe or linkedin.com/in/janedoe"
    linkedin = RedactionPatterns.find_linkedin(text)
    assert len(linkedin) >= 1


def test_find_portfolios():
    """Test portfolio URL detection"""
    text = "Check my work at https://github.com/johndoe and https://behance.net/janedoe"
    portfolios = RedactionPatterns.find_portfolios(text)
    assert len(portfolios) >= 1


def test_get_redaction_items():
    """Test comprehensive redaction item detection"""
    text = """
    John Doe
    Email: john@example.com
    Phone: (555) 123-4567
    LinkedIn: https://linkedin.com/in/johndoe
    Portfolio: https://github.com/johndoe
    """

    items = RedactionPatterns.get_redaction_items(
        text,
        ['email', 'phone', 'linkedin', 'portfolio']
    )

    assert len(items['emails']) > 0
    assert len(items['phones']) > 0
    assert len(items['linkedin']) > 0
    assert len(items['portfolios']) > 0
