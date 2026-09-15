"""Semantic translation from technical indicator outputs to specialist evidence.

The adapter deliberately performs no indicator calculation. It consumes the
canonical ``IndicatorResult`` shape by protocol, applies an explicit mapping
policy, and emits the normalized evidence consumed by the single consensus
boundary. Unsupported indicators fail closed instead of silently inventing a
trading interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal, Protocol

from .consensus import Direction, SpecialistEvidence


class IndicatorResultLike(Protocol):
    """Minimal dependency-free view of a canonical indicator result."""

    name: str
    values: tuple[float | None, ...]
    warmup: int


MappingMode = Literal["centered", "inverted_centered", "price_relation"]


@dataclass(frozen=True, slots=True)
class IndicatorEvidencePolicy:
    """Explicit semantic mapping policy for one indicator output."""

    indicator_name: str
    mode: MappingMode
    center: float = 0.0
    deadband: float = 0.0
    scale: float = 1.0

    def __post_init__(self) -> None:
        if not self.indicator_name.strip():
            raise ValueError("indicator_name is required")
        if not isfinite(self.center) or not isfinite(self.deadband) or not isfinite(self.scale):
            raise ValueError("policy values must be finite")
        if self.deadband < 0.0:
            raise ValueError("deadband must be >= 0")
        if self.scale <= 0.0:
            raise ValueError("scale must be > 0")


# Only outputs whose directional interpretation is explicit are registered.
# Volatility, bands, channels, volume totals and structural components require
# additional context and are intentionally not auto-translated here.
DEFAULT_INDICATOR_EVIDENCE_POLICIES: tuple[IndicatorEvidencePolicy, ...] = (
    IndicatorEvidencePolicy("rsi", "centered", center=50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("stochastic.k", "centered", center=50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("stochastic.d", "centered", center=50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("williams.r", "inverted_centered", center=-50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("cci", "centered", center=0.0, deadband=25.0, scale=200.0),
    IndicatorEvidencePolicy("mfi", "centered", center=50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("stochastic_rsi", "centered", center=50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("stochastic_rsi.signal", "centered", center=50.0, deadband=5.0, scale=50.0),
    IndicatorEvidencePolicy("momentum", "centered", center=0.0, deadband=0.0, scale=1.0),
    IndicatorEvidencePolicy("roc", "centered", center=0.0, deadband=0.0, scale=100.0),
    IndicatorEvidencePolicy("trix", "centered", center=0.0, deadband=0.0, scale=1.0),
    IndicatorEvidencePolicy("macd.histogram", "centered", center=0.0, deadband=0.0, scale=1.0),
)


class IndicatorEvidenceAdapter:
    """Convert a canonical indicator output into one specialist contribution."""

    def __init__(
        self,
        policies: tuple[IndicatorEvidencePolicy, ...] = DEFAULT_INDICATOR_EVIDENCE_POLICIES,
    ) -> None:
        policy_map = {policy.indicator_name: policy for policy in policies}
        if len(policy_map) != len(policies):
            raise ValueError("indicator evidence policy names must be unique")
        self._policies = policy_map

    def to_evidence(
        self,
        result: IndicatorResultLike,
        *,
        data_revision: str,
        confidence: float,
        weight: float = 1.0,
        source_id: str | None = None,
    ) -> SpecialistEvidence:
        """Translate the latest available output without recalculating it."""
        if not data_revision.strip():
            raise ValueError("data_revision is required")
        if not isfinite(confidence) or not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be finite and between 0 and 1")
        if not isfinite(weight) or weight <= 0.0:
            raise ValueError("weight must be finite and > 0")
        policy = self._policies.get(result.name)
        if policy is None:
            raise ValueError(f"no directional evidence policy for indicator {result.name!r}")
        if result.warmup < 0 or result.warmup > len(result.values):
            raise ValueError("indicator warmup is outside result bounds")

        latest = next((value for value in reversed(result.values) if value is not None), None)
        if latest is None:
            raise ValueError(f"indicator {result.name!r} has no usable value")
        if not isfinite(latest):
            raise ValueError("indicator value must be finite")

        delta = latest - policy.center
        if abs(delta) <= policy.deadband:
            direction: Direction = "neutral"
            strength = 0.0
        else:
            if policy.mode == "inverted_centered":
                delta = -delta
            direction = "bullish" if delta > 0.0 else "bearish"
            strength = min(1.0, abs(delta) / policy.scale)

        return SpecialistEvidence(
            source_id=source_id or f"indicator:{result.name}",
            direction=direction,
            strength=strength,
            confidence=confidence,
            weight=weight,
            data_revision=data_revision,
        )


__all__ = [
    "DEFAULT_INDICATOR_EVIDENCE_POLICIES",
    "IndicatorEvidenceAdapter",
    "IndicatorEvidencePolicy",
    "IndicatorResultLike",
]
