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
    assert first.contributors == ("atr", "macd", "rsi")
    assert first.score > 0.0
    assert first.agreement > 0.5
    assert not first.abstained


def test_consensus_abstains_on_close_disagreement() -> None:
    service = AnalysisConsensusService(minimum_confidence=0.4, minimum_margin=0.25)
    result = service.aggregate(
        (
            evidence("a", "bullish", 1.0, 1.0),
            evidence("b", "bearish", 1.0, 1.0),
        )
    )
    assert result.direction == "neutral"
    assert result.abstained
    assert result.reason == "insufficient_margin"
    assert result.score == 0.0
    assert result.agreement == 0.5


def test_consensus_distinguishes_directional_score_from_agreement() -> None:
    result = AnalysisConsensusService(minimum_confidence=0.0, minimum_margin=0.0).aggregate(
        (
            evidence("strong-bull", "bullish", 1.0, 1.0),
            evidence("weak-bear", "bearish", 0.2, 1.0),
            evidence("context", "neutral", 1.0, 1.0),
        )
    )
    assert result.direction == "bullish"
    assert result.score == pytest.approx(2.0 / 3.0)
    assert result.agreement == pytest.approx(1.0 / 1.2)
    assert not result.abstained


def test_consensus_abstains_without_directional_evidence() -> None:
    result = AnalysisConsensusService().aggregate(
        (evidence("context", "neutral", 1.0, 1.0),)
    )
    assert result.direction == "neutral"
    assert result.abstained
    assert result.reason == "no_directional_evidence"
    assert result.score == 0.0
    assert result.agreement == 0.0


def test_consensus_rejects_mixed_revisions() -> None:
    with pytest.raises(ValueError, match="same data_revision"):
        AnalysisConsensusService().aggregate(
            (
                evidence("a", "bullish", 1.0, 1.0),
                SpecialistEvidence("b", "bullish", 1.0, 1.0, 1.0, "rev-002"),
            )
        )


def test_consensus_rejects_duplicate_sources() -> None:
    with pytest.raises(ValueError, match="source_id must be unique"):
        AnalysisConsensusService().aggregate(
            (
                evidence("rsi", "bullish", 1.0, 1.0),
                evidence("rsi", "bullish", 1.0, 1.0),
            )
        )


def test_consensus_rejects_invalid_weights() -> None:
    with pytest.raises(ValueError, match="weight"):
        SpecialistEvidence("bad", "bullish", 1.0, 1.0, 0.0, "rev-001")
