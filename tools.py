"""
Pure Python re-implementations of the small calculators that lived in
columns D/E of the index sheet. No UI code here — app.py imports these.
"""

from __future__ import annotations

from datetime import date


def sitting_height(total_height_cm: float, stool_height_cm: float = 47.5) -> float:
    """Mirrors: sitting height = total height - stool height."""
    return total_height_cm - stool_height_cm


def duration_percentage(duration_months: float, max_duration_months: float) -> float:
    """Mirrors: = (duration / max_duration) * 100. Returns 0 if max is 0."""
    if not max_duration_months:
        return 0.0
    return (duration_months / max_duration_months) * 100


def months_between(start: date, end: date) -> int:
    """
    Complete months between two dates, matching Excel's DATEDIF(start, end, "M").
    Order-independent: pass dates in either order.
    """
    if end < start:
        start, end = end, start
    months = (end.year - start.year) * 12 + (end.month - start.month)
    if end.day < start.day:
        months -= 1
    return max(months, 0)


def months_since(start: date, today: date | None = None) -> int:
    """Mirrors: = DATEDIF(start_date, TODAY(), "M")."""
    return months_between(start, today or date.today())
