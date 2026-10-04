"""Tiny slug helper used by the blog."""
import re


def slugify(title: str, max_len: int = 60) -> str:
    """Lower-case, ASCII, hyphen-separated slug.

    >>> slugify("Hello, World!")
    'hello-world'
    >>> slugify("  Ação & Reação ")
    'acao-reacao'
    """
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s[:max_len]
