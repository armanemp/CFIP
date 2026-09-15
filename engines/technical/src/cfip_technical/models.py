"""Typed market inputs and immutable indicator outputs."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class OHLCV:
    """One ordered market observation.

    Values are floats intentionally: the technical engine is a numerical
    analytics boundary, while price/account monetary semantics belong to the
    financial domain and must not be inferred from this type.
    """

    open: float
    high: float
    low: float
    close: float
    volume: float | None = None

    def __post_init__(self) -> None:
        values = (self.open, self.high, self.low, self.close)
        if not all(isfinite(value) for value in values):
            raise ValueError("OHLC values must be finite")
        if self.high < max(self.open, self.close) or self.low > min(self.open, self.close):
            raise ValueError("OHLC bounds are inconsistent")
        if self.volume is not None and (not isfinite(self.volume) or self.volume < 0):
            raise ValueError("volume must be finite and >= 0")


@dataclass(frozen=True, slots=True)
class IndicatorResult:
    """Immutable indicator series with explicit warm-up metadata."""

    name: str
    period: int
    values: tuple[float | None, ...]
    warmup: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name is required")
        if self.period <= 0:
            raise ValueError("period must be > 0")
        if self.warmup < 0 or self.warmup > len(self.values):
            raise ValueError("warmup is outside result bounds")
