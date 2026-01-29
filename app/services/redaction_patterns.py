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
    # These patterns are designed to be specific to actual phone numbers and NOT match:
    # - Years (2020, 2024)
    # - GPA scores (3.5, 4.0)
    # - Dates (01/15/2024)
    # - Short number sequences
    PHONE_PATTERNS = [
        # International format with + prefix (required for international)
        # e.g., +1-555-123-4567, +91 9876543210, +44 20 7946 0958
        re.compile(r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{3,4}[-.\s]?\d{0,4}'),
        # US format with area code in parentheses: (xxx) xxx-xxxx
        re.compile(r'\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}'),
        # US format with separators: xxx-xxx-xxxx or xxx.xxx.xxxx
        re.compile(r'(?<!\d)\d{3}[-.\s]\d{3}[-.\s]\d{4}(?!\d)'),
        # 10-digit number with clear phone context (standalone, not part of larger number)
        # Only match if surrounded by non-digit characters
        re.compile(r'(?<![.\d])\d{10}(?![.\d])'),
        # Indian format: +91 followed by 10 digits
        re.compile(r'\+91[-.\s]?\d{5}[-.\s]?\d{5}'),
        # Format with country code without +: 91-xxx-xxx-xxxx
        re.compile(r'(?<!\d)91[-.\s]\d{3,5}[-.\s]\d{3,5}[-.\s]?\d{0,4}(?!\d)'),
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

        # Filter out false positives
        filtered_phones = []
        for phone in phones:
            # Remove any whitespace and separators to count digits
            digits_only = re.sub(r'[^\d]', '', phone)

            # Skip if too few digits (less than 7) - not a valid phone
            if len(digits_only) < 7:
                continue

            # Skip if it looks like a year (4 digits, starting with 19 or 20)
            if len(digits_only) == 4 and (digits_only.startswith('19') or digits_only.startswith('20')):
                continue

            # Skip if it looks like a year range pattern (e.g., "2020" alone)
            clean_phone = phone.strip()
            if re.match(r'^(19|20)\d{2}$', clean_phone):
                continue

            # Skip common false positives - pure years
            if re.match(r'^(19|20)\d{2}[-–]\s*(19|20)?\d{2}$', clean_phone):
                continue

            filtered_phones.append(phone)

        return list(set(filtered_phones))  # Remove duplicates

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
