import re


def parse_duration(text: str) -> int:
    m = re.fullmatch(r"(?:(\d+)h)? ?(?:(\d+)m)? ?(?:(\d+)s)?", text.strip(), re.I)
    if not m or not any(m.groups()):
        raise ValueError(f"invalid duration: {text!r}")
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mi * 60 + s
