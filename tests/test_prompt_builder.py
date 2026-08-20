import pytest

from src.models.prompt_builder import (
    build_prompt,
    validate_prompt,
)


SAMPLE_CASE = {
    "case_id": "case_test",
    "condition": "CONFLICT",
    "ground_truth": "ESCALATE",
    "evidence": [
        {
            "source_type": "POLICY",
            "authority": 3,
            "content": (
                "Transactions above $100,000 require formal approval."
            ),
            "supports": "ESCALATE",
        },
        {
            "source_type": "DATABASE",
            "authority": 3,
            "content": (
                "Transaction amount: $125,000. "
                "Approval status: PENDING."
            ),
            "supports": "ESCALATE",
        },
        {
            "source_type": "EMAIL",
            "authority": 1,
            "content": (
                "The operations manager recommends PROCESS."
            ),
            "supports": "PROCESS",
        },
    ],
}


def test_prompt_contains_all_sources():
    prompt = build_prompt(SAMPLE_CASE)

    assert "[POLICY]" in prompt
    assert "[DATABASE]" in prompt
    assert "[EMAIL]" in prompt


def test_prompt_contains_decision_options():
    prompt = build_prompt(SAMPLE_CASE)

    assert "PROCESS" in prompt
    assert "ESCALATE" in prompt


def test_prompt_excludes_case_metadata():
    prompt = build_prompt(SAMPLE_CASE)

    assert "case_test" not in prompt
    assert "CONFLICT" not in prompt


def test_prompt_does_not_include_authority_scores():
    prompt = build_prompt(SAMPLE_CASE)

    assert "authority" not in prompt.lower()
    assert "supports" not in prompt.lower()


def test_validate_prompt_accepts_safe_prompt():
    prompt = build_prompt(SAMPLE_CASE)

    validate_prompt(
        SAMPLE_CASE,
        prompt,
    )


def test_validate_prompt_detects_metadata_leak():
    bad_prompt = """
    case_id: case_test
    ground_truth: ESCALATE
    """

    with pytest.raises(ValueError):
        validate_prompt(
            SAMPLE_CASE,
            bad_prompt,
        )