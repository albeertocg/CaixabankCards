import re

_INJECTION_PATTERNS = [
    re.compile(r"ignor[ae]\s+(todas?\s+las?\s+)?instrucciones?", re.IGNORECASE),
    re.compile(r"ignore\s+(all\s+)?(previous\s+)?instructions?", re.IGNORECASE),
    re.compile(r"olvida\s+(todo|tus\s+instrucciones)", re.IGNORECASE),
    re.compile(r"forget\s+(everything|your\s+instructions?)", re.IGNORECASE),
    re.compile(
        r"(eres|act[uú]a\s+como|ahora\s+eres)\s+(un|una|el|la)\s+", re.IGNORECASE
    ),
    re.compile(r"(you\s+are|act\s+as|pretend\s+to\s+be)\s+", re.IGNORECASE),
    re.compile(
        r"(system\s*prompt|instrucciones?\s+internas?|prompt\s+del?\s+sistema)",
        re.IGNORECASE,
    ),
    re.compile(
        r"\[/?INST\]|\[/?SYS(TEM)?\]|<\|?(im_start|im_end|system|assistant)\|?>",
        re.IGNORECASE,
    ),
    re.compile(
        r"(repite|muestra|dime|revela|show|reveal|repeat)\s+.{0,20}(system|instrucciones?|prompt)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(nuevo\s+rol|new\s+role|modo\s+developer|developer\s+mode)", re.IGNORECASE
    ),
    re.compile(r"(jailbreak|DAN\b|do\s+anything\s+now)", re.IGNORECASE),
]


def sanitize_text(text: str) -> str:
    cleaned = text
    for pattern in _INJECTION_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def contains_injection(text: str) -> bool:
    return any(pattern.search(text) for pattern in _INJECTION_PATTERNS)
