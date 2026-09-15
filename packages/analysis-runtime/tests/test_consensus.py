from __future__ import annotations

import pytest

from cfip_analysis_runtime.consensus import AnalysisConsensusService, SpecialistEvidence


def evidence(source: str, direction: str, strength: float, confidence: float, weight: float = 1.0) -> SpecialistEvidence:
    return SpecialistEvidence(source, direction, strength, confidence, weight, "rev-001")  # type: ignore[arg-type]


def test_consensus_is_deterministic_and_preserves_revision() -> None:
    service = AnalysisConsensusService(minimum_confidence=0.4, minimum_margin=0.05)
    inputs = (
        evidence("rsi", "bullish", 0.9, 0.9),
        evidence("macd", "bullish", 0.8, 0.8),
        evidence("atr", "bearish", 0.2, 0.7),
    )
    first = service.aggregate(inputs)
    second = service.aggregate(inputs)
    assert first == second
    assert first.direction == "bullish"
    assert first.data_revision == "rev-001"
    assert not first.abstained


def test_consensus_abstains_on_close_disagreement() -> None:
    service = AnalysisConsensusService(minimum_confidence=0.4, minimum_margin=0.25)
    result = service.aggregate((
        evidence("a", "bullish", 1.0, 1.0),
        evidence("b", "bearish", 1.0, 1.0),
    ))
    assert result.direction == "neutral"
    assert result.abstained
    assert result.reason == "insufficient_margin"


def test_consensus_rejects_mixed_revisions() -> None:
    with pytest.raises(ValueError, match="same data_revision"):
        AnalysisConsensusService().aggregate((
            evidence("a", "bullish", 1.0, 1.0),
            SpecialistEvidence("b", "bullish", 1.0, 1.0, 1.0, "rev-002"),
        ))


def test_consensus_rejects_invalid_weights() -> None:
    with pytest.raises(ValueError, match="weight"):
        SpecialistEvidence("bad", "bullish", 1.0, 1.0, 0.0, "rev-001")
