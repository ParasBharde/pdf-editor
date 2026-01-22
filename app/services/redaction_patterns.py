"""
Regex patterns for detecting sensitive information in PDFs
"""
import re

class RedactionPatterns:
    """
    Defines regex patterns for identifying sensitive information
    """

    # Email pattern
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        re.IGNORECASE
    )

    # Phone number patterns (supports various formats)
    PHONE_PATTERNS = [
        re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'),  # International
        re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),  # US format (xxx) xxx-xxxx
        re.compile(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'),  # xxx-xxx-xxxx
        re.compile(r'\d{10,}'),  # 10+ consecutive digits
    ]

    # LinkedIn URL pattern
    LINKEDIN_PATTERN = re.compile(
        r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?',
        re.IGNORECASE
    )

    # Portfolio/Website URLs
    PORTFOLIO_PATTERNS = [
        re.compile(r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+/?', re.IGNORECASE),
        re.compile(r'(?:https?://)?(?:www\.)?behance\.net/[A-Za-z0-9_-]+/?', re.IGNORECASE),
        re.compile(r'(?:https?://)?(?:www\.)?dribbble\.com/[A-Za-z0-9_-]+/?', re.IGNORECASE),
        re.compile(r'(?:https?://)?(?:www\.)?portfolio\.com/[A-Za-z0-9_-]+/?', re.IGNORECASE),
        re.compile(r'(?:https?://)?[A-Za-z0-9.-]+\.(?:com|net|org|io|dev|me|co)/?\S*', re.IGNORECASE),
    ]

    # Generic URL pattern (fallback)
    URL_PATTERN = re.compile(
        r'(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?',
        re.IGNORECASE
    )

    @classmethod
    def find_emails(cls, text):
        """Find all email addresses in text"""
        return cls.EMAIL_PATTERN.findall(text)

    @classmethod
    def find_phones(cls, text):
        """Find all phone numbers in text"""
        phones = []
        for pattern in cls.PHONE_PATTERNS:
            matches = pattern.findall(text)
            phones.extend(matches)
        return list(set(phones))  # Remove duplicates

    @classmethod
    def find_linkedin(cls, text):
        """Find LinkedIn URLs in text"""
        return cls.LINKEDIN_PATTERN.findall(text)

    @classmethod
    def find_portfolios(cls, text):
        """Find portfolio/website URLs in text"""
        portfolios = []
        for pattern in cls.PORTFOLIO_PATTERNS:
            matches = pattern.findall(text)
            portfolios.extend(matches)
        return list(set(portfolios))

    @classmethod
    def find_all_urls(cls, text):
        """Find all URLs in text"""
        return cls.URL_PATTERN.findall(text)

    @classmethod
    def get_redaction_items(cls, text, redaction_types):
        """
        Get all items to redact based on specified types

        Args:
            text: The text to search
            redaction_types: List of types to redact (email, phone, linkedin, portfolio, all_urls)

        Returns:
            Dictionary with found items
        """
        items = {
            'emails': [],
            'phones': [],
            'linkedin': [],
            'portfolios': [],
            'urls': []
        }

        if 'email' in redaction_types:
            items['emails'] = cls.find_emails(text)

        if 'phone' in redaction_types:
            items['phones'] = cls.find_phones(text)

        if 'linkedin' in redaction_types:
            items['linkedin'] = cls.find_linkedin(text)

        if 'portfolio' in redaction_types:
            items['portfolios'] = cls.find_portfolios(text)

        if 'all_urls' in redaction_types:
            items['urls'] = cls.find_all_urls(text)

        return items
