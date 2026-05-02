"""
utils/helpers.py — Shared utility functions
"""
import uuid
from datetime import datetime


def generate_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def truncate_text(text: str, max_chars: int = 300) -> str:
    """Return a preview of the text, truncated at word boundary."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_space = truncated.rfind(" ")
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated + "…"
