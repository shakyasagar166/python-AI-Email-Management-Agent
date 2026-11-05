"""
Email Parsing & Text Cleaning Utilities
"""
import re
import html
from typing import Dict, Any


def clean_text_content(raw_text: str) -> str:
    """Strip excess formatting, unescape HTML entities, normalize linebreaks."""
    if not raw_text:
        return ""
    text = html.unescape(raw_text)
    # Remove HTML tags if present in plain text
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def extract_email_snippet(body_text: str, max_chars: int = 150) -> str:
    """Generate a clean single-line snippet for preview list items."""
    clean = clean_text_content(body_text)
    clean = re.sub(r"\s+", " ", clean)
    if len(clean) > max_chars:
        return clean[:max_chars].strip() + "..."
    return clean


def parse_sender_header(sender_str: str) -> Dict[str, str]:
    """Parse 'John Doe <john@example.com>' into name and email components."""
    if not sender_str:
        return {"name": "Unknown", "email": ""}
    match = re.match(r"^(.*?)\s*<([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>\s*$", sender_str.strip())
    if match:
        name = match.group(1).strip(' "\'')
        return {"name": name or match.group(2), "email": match.group(2).lower()}
    # Fallback if bare email
    if "@" in sender_str:
        email = sender_str.strip().lower()
        name = email.split("@")[0].replace(".", " ").title()
        return {"name": name, "email": email}
    return {"name": sender_str.strip(), "email": ""}
