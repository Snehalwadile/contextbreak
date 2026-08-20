VALID_DECISIONS = {"PROCESS", "ESCALATE"}


def parse_response(text: str) -> str:
    """
    Parse a model response into one valid decision.
    """

    normalized = text.strip().upper()

    if normalized in VALID_DECISIONS:
        return normalized

    raise ValueError(
        f"Invalid model response: {text!r}"
    )