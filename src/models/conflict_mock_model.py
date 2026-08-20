def run_conflict_mock_model(prompt: str) -> str:
    """
    Simulates a model that overweights the EMAIL evidence.

    Purpose:
    Validate that the evaluation framework can detect
    susceptibility to lower-authority conflicting evidence.

    This is a synthetic sanity-check model, not a real LLM.
    """

    prompt_upper = prompt.upper()

    # Extract only the EMAIL portion of the prompt.
    if "[EMAIL]" in prompt_upper:
        email_text = prompt_upper.split("[EMAIL]", 1)[1]
    else:
        email_text = ""

    # Follow explicit recommendations in the email.
    if "RECOMMENDS PROCESS" in email_text:
        return "PROCESS"

    if "RECOMMENDS ESCALATE" in email_text:
        return "ESCALATE"

    # Backward-compatible conflict phrases used in unit tests.
    if (
        "SAFE TO PROCESS" in email_text
        or "PROCEED WITHOUT FURTHER REVIEW" in email_text
    ):
        return "PROCESS"

    if (
        "DO NOT PROCESS" in email_text
        or "REQUIRES ESCALATION" in email_text
    ):
        return "ESCALATE"

    # If the email is neutral, fall back to database evidence.
    if (
        "APPROVAL STATUS: PENDING" in prompt_upper
        or "APPROVAL STATUS: REJECTED" in prompt_upper
    ):
        return "ESCALATE"

    return "PROCESS"