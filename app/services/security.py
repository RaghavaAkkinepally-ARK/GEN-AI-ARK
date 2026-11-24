import re
from typing import Iterable


INJECTION_PATTERNS = (
    r"ignore\s+(all\s+)?(previous|system)\s+instructions",
    r"reveal\s+(the\s+)?(system\s+)?prompt",
    r"send\s+.*(api[_ -]?key|secret|password)",
)

SENSITIVE_PATTERNS = (
    r"\bsk-[A-Za-z0-9_-]{8,}\b",
    r"\bpassword\s*[:=]\s*\S+",
)


def contains_prompt_injection(text: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in INJECTION_PATTERNS)


def contains_sensitive_data(text: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in SENSITIVE_PATTERNS)


def redact_sensitive(text: str) -> str:
    for pattern in SENSITIVE_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text, flags=re.I)
    return text

