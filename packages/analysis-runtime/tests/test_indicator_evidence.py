from dataclasses import dataclass

import pytest

from cfip_analysis_runtime import IndicatorEvidenceAdapter


@dataclass(frozen=True)
class Result:
    name: str
    values: tuple[float | None, ...]
    warmup: int


def test_adapter_uses_latest_non_missing_value_without_recalculation() -> None:
    result = Result("rsi", (None, 42.0, 48.0, 62.0), 1)

    evidence = IndicatorEvidenceAdapter().to_evidence(
        result,
        data_revision="bars:eurusd:15m:100",
        confidence=0.9,
    )

    assert evidence.source_id == "indicator:rsi"
    assert evidence.direction == "bullish"
    assert evidence.strength == pytest.approx(0.24)
    assert evidence.confidence == 0.9


def test_centered_deadband_abstains_directionally() -> None:
    result = Result("cci", (None, 12.0), 1)

    evidence = IndicatorEvidenceAdapter().to_evidence(
        result,
        data_revision="bars:eurusd:15m:101",
        confidence=0.8,
    )

    assert evidence.direction == "neutral"
    assert evidence.strength == 0.0


def test_williams_is_explicitly_inverted() -> None:
    result = Result("williams.r", (-30.0,), 0)

    evidence = IndicatorEvidenceAdapter().to_evidence(
        result,
        data_revision="bars:eurusd:15m:102",
        confidence=1.0,
    )

    assert evidence.direction == "bearish"
    assert evidence.strength == pytest.approx(0.4)


def test_unsupported_indicator_fails_closed() -> None:
    result = Result("atr", (1.2,), 0)

    with pytest.raises(ValueError, match="no directional evidence policy"):
        IndicatorEvidenceAdapter().to_evidence(
            result,
            data_revision="bars:eurusd:15m:103",
            confidence=1.0,
        )


def test_empty_indicator_output_fails_closed() -> None:
    result = Result("rsi", (None, None), 2)

    with pytest.raises(ValueError, match="no usable value"):
        IndicatorEvidenceAdapter().to_evidence(
            result,
            data_revision="bars:eurusd:15m:104",
            confidence=1.0,
        )
