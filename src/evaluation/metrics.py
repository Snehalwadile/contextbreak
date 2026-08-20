def conflict_sensitivity(
    accuracy: dict[str, float],
) -> float:
    """
    Measure the accuracy drop caused by conflicting evidence.

    Positive values mean conflict hurts performance.
    Zero means no measurable effect.
    Negative values mean conflict unexpectedly improves performance.
    """

    return (
        accuracy["CLEAN"]
        - accuracy["CONFLICT"]
    )