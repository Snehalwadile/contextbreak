import pytest

from src.models.response_parser import parse_response


def test_parse_process():
    assert parse_response("PROCESS") == "PROCESS"


def test_parse_escalate():
    assert parse_response("ESCALATE") == "ESCALATE"


def test_parse_ignores_whitespace():
    assert parse_response("  PROCESS  ") == "PROCESS"


def test_parse_ignores_case():
    assert parse_response("escalate") == "ESCALATE"


def test_parse_rejects_invalid_response():
    with pytest.raises(ValueError):
        parse_response(
            "I think this should probably be processed."
        )