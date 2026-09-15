"""Shared primitives for deterministic technical indicators."""

from __future__ import annotations

from typing import Sequence

from .models import OHLCV


def validate_period(period: int) -> None:
    """Reject invalid rolling-window periods consistently across families."""
    if period <= 0:
        raise ValueError("period must be > 0")


def closes(data: Sequence[OHLCV]) -> tuple[float, ...]:
    """Return the close series without introducing mutable shared state."""
    return tuple(item.close for item in data)
