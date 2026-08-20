import pytest
from src.evaluation.metrics import conflict_sensitivity


def test_conflict_sensitivity():
    accuracy = {
        "CLEAN": 0.90,
        "CONFLICT": 0.70,
        "NEUTRAL": 0.85,
    }

    result = conflict_sensitivity(
        accuracy
    )

    assert result == pytest.approx(0.20)


def test_zero_conflict_sensitivity():
    accuracy = {
        "CLEAN": 0.80,
        "CONFLICT": 0.80,
        "NEUTRAL": 0.80,
    }

    result = conflict_sensitivity(
        accuracy
    )

    assert result == 0.0