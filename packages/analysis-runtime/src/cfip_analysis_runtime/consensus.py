"""Deterministic specialist-evidence consensus boundary.

This module is the single aggregation authority for directional specialist
outputs. It does not know about indicators, brokers, databases or AI models.
Identical inputs, weights and policy produce identical results.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal

Direction = Literal["bullish", "bearish", "neutral"]


@dataclass(frozen=True, slots=True)
class SpecialistEvidence:
    """One normalized specialist contribution to consensus."""

    source_id: str
    direction: Direction
    strength: float
    confidence: float
    weight: float = 1.0
    data_revision: str = ""

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if self.direction not in {"bullish", "bearish", "neutral"}:
            raise ValueError("unsupported direction")
        for name, value in (("strength", self.strength), ("confidence", self.confidence), ("weight", self.weight)):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be finite and between 0 and 1")
        if self.weight <= 0:
            raise ValueError("weight must be > 0")
        if not self.data_revision.strip():
            raise ValueError("data_revision is required")


@dataclass(frozen=True, slots=True)
class ConsensusResult:
    """Reproducible aggregate result with explicit abstention/disagreement."""

    direction: Direction
    score: float
    confidence: float
    agreement: float
    contributors: tuple[str, ...]
    data_revision: str
    abstained: bool
    reason: str | None = None


class AnalysisConsensusService:
    """Aggregate normalized specialist evidence with bounded abstention."""

    def __init__(self, *, minimum_confidence: float = 0.5, minimum_margin: float = 0.1) -> None:
        if not 0.0 <= minimum_confidence <= 1.0:
            raise ValueError("minimum_confidence must be between 0 and 1")
        if not 0.0 <= minimum_margin <= 1.0:
            raise ValueError("minimum_margin must be between 0 and 1")
        self._minimum_confidence = minimum_confidence
        self._minimum_margin = minimum_margin

    def aggregate(self, evidence: tuple[SpecialistEvidence, ...]) -> ConsensusResult:
        if not evidence:
            raise ValueError("at least one specialist evidence item is required")

        revisions = {item.data_revision for item in evidence}
        if len(revisions) != 1:
            raise ValueError("all specialist evidence must use the same data_revision")
        revision = next(iter(revisions))

        totals = {"bullish": 0.0, "bearish": 0.0, "neutral": 0.0}
        confidence_mass = 0.0
        for item in evidence:
            contribution = item.weight * item.strength * item.confidence
            totals[item.direction] += contribution
            confidence_mass += item.weight * item.confidence

        total_weight = sum(item.weight for item in evidence)
        dominant = max(totals, key=totals.__getitem__)
        ordered = sorted(totals.values(), reverse=True)
        dominant_mass = ordered[0]
        runner_up = ordered[1]
        normalized_score = dominant_mass / sum(totals.values()) if sum(totals.values()) else 0.0
        agreement = dominant_mass / (sum(totals.values()) or 1.0)
        confidence = confidence_mass / total_weight
        margin = dominant_mass / (total_weight or 1.0) - runner_up / (total_weight or 1.0)

        abstained = (
            dominant == "neutral"
            or confidence < self._minimum_confidence
            or margin < self._minimum_margin
        )
        if abstained:
            reason = "insufficient_confidence" if confidence < self._minimum_confidence else "insufficient_margin"
            return ConsensusResult(
                direction="neutral",
                score=normalized_score,
                confidence=confidence,
                agreement=agreement,
                contributors=tuple(item.source_id for item in evidence),
                data_revision=revision,
                abstained=True,
                reason=reason,
            )

        return ConsensusResult(
            direction=dominant,
            score=normalized_score,
            confidence=confidence,
            agreement=agreement,
            contributors=tuple(item.source_id for item in evidence),
            data_revision=revision,
            abstained=False,
        )
