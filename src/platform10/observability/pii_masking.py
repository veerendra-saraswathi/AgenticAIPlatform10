import re
from typing import Any, Dict


# --- Simple but effective PII patterns (extend later) ---
PAN_PATTERN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")
AADHAAR_PATTERN = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_PATTERN = re.compile(r"\b\d{10}\b")


def _mask_string(value: str) -> str:
    value = PAN_PATTERN.sub("[PAN_REDACTED]", value)
    value = AADHAAR_PATTERN.sub("[AADHAAR_REDACTED]", value)
    value = EMAIL_PATTERN.sub("[EMAIL_REDACTED]", value)
    value = PHONE_PATTERN.sub("[PHONE_REDACTED]", value)
    return value


def mask_pii(data: Any) -> Any:
    """
    Recursively mask PII in dicts, lists, and strings.
    """
    if isinstance(data, str):
        return _mask_string(data)

    if isinstance(data, list):
        return [mask_pii(item) for item in data]

    if isinstance(data, dict):
        return {key: mask_pii(value) for key, value in data.items()}

    return data

