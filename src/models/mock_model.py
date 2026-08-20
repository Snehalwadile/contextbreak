def run_mock_model(prompt: str) -> str:
    """
    Temporary deterministic model used to test
    the evaluation pipeline without API calls.
    """

    if "Approval status: PENDING" in prompt:
        return "ESCALATE"

    if "Approval status: REJECTED" in prompt:
        return "ESCALATE"

    return "PROCESS"