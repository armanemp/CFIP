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
ConflictClass = Literal["aligned", "mixed", "neutral"]


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
            if not isfinite(value) or value < 0.0 or value > 1.0:
                raise ValueError(f"{name} must be finite and between 0 and 1")
        if self.weight <= 0:
            raise ValueError("weight must be > 0")
        if not self.data_revision.strip():
            raise ValueError("data_revision is required")


@dataclass(frozen=True, slots=True)
class ConsensusResult:
    """Reproducible aggregate result with explicit conflict and abstention."""

    direction: Direction
    score: float
    confidence: float
    agreement: float
    contributors: tuple[str, ...]
    data_revision: str
    abstained: bool
    reason: str | None = None
    conflict: ConflictClass = "neutral"
    explanation: tuple[str, ...] = ()


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
        source_ids = [item.source_id for item in evidence]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("source_id must be unique within one consensus set")

        revision = next(iter(revisions))
        totals = {"bullish": 0.0, "bearish": 0.0, "neutral": 0.0}
        confidence_mass = 0.0
        for item in evidence:
            contribution = item.weight * item.strength * item.confidence
            totals[item.direction] += contribution
            confidence_mass += item.weight * item.confidence

        total_weight = sum(item.weight for item in evidence)
        directional_mass = totals["bullish"] + totals["bearish"]
        dominant = max(totals, key=totals.__getitem__)
        ordered = sorted(totals.values(), reverse=True)
        dominant_mass, runner_up = ordered[0], ordered[1]
        confidence = confidence_mass / total_weight
        if directional_mass:
            score = (totals["bullish"] - totals["bearish"]) / directional_mass
            agreement = max(totals["bullish"], totals["bearish"]) / directional_mass
        else:
            score = 0.0
            agreement = 0.0
        margin = (dominant_mass - runner_up) / total_weight

        if directional_mass == 0.0:
            conflict: ConflictClass = "neutral"
            reason = "no_directional_evidence"
        elif dominant == "neutral":
            conflict = "neutral"
            reason = "neutral_consensus"
        elif margin < self._minimum_margin:
            conflict = "mixed"
            reason = "insufficient_margin"
        else:
            conflict = "aligned"
            reason = None
        if reason is None and confidence < self._minimum_confidence:
            reason = "insufficient_confidence"

        abstained = reason is not None
        explanation = (
            f"directional_mass={directional_mass:.6f}",
            f"confidence={confidence:.6f}",
            f"agreement={agreement:.6f}",
            f"margin={margin:.6f}",
            f"conflict={conflict}",
        )
        return ConsensusResult(
            direction="neutral" if abstained else dominant,
            score=score,
            confidence=confidence,
            agreement=agreement,
            contributors=tuple(sorted(source_ids)),
            data_revision=revision,
            abstained=abstained,
            reason=reason,
            conflict=conflict,
            explanation=explanation,
        )


__all__ = ["AnalysisConsensusService", "ConflictClass", "ConsensusResult", "Direction", "SpecialistEvidence"]
