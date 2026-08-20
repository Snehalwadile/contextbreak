from typing import Any


VALID_DECISIONS = ("PROCESS", "ESCALATE")


def build_prompt(case: dict[str, Any]) -> str:
    """
    Convert one experimental case into a standardized LLM prompt.

    Evaluation-only metadata is intentionally excluded.
    """

    evidence_sections = []

    for item in case["evidence"]:
        evidence_sections.append(
            f"[{item['source_type']}]\n"
            f"{item['content']}"
        )

    evidence_text = "\n\n".join(evidence_sections)

    prompt = f"""You are reviewing a financial transaction.

Use the available evidence to determine the correct action.

Evidence:

{evidence_text}

Choose exactly one action:

PROCESS
ESCALATE

Return only the action."""

    return prompt


def validate_prompt(
    case: dict[str, Any],
    prompt: str,
) -> None:
    """
    Ensure evaluation-only metadata fields are not exposed
    to the model.
    """

    forbidden_metadata = [
        "ground_truth",
        "case_id",
        "condition",
        "authority",
        "supports",
    ]

    prompt_lower = prompt.lower()

    for field in forbidden_metadata:
        if field.lower() in prompt_lower:
            raise ValueError(
                f"Evaluation metadata leaked into prompt: {field}"
            )