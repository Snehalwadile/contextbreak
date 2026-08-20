import json
from collections import defaultdict
from pathlib import Path


def load_results(
    path: str,
) -> list[dict]:
    """
    Load model evaluation results from JSONL.
    """

    results = []

    with Path(path).open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            if line.strip():
                results.append(
                    json.loads(line)
                )

    return results


def paired_conflict_analysis(
    results: list[dict],
) -> dict:
    """
    Compare CLEAN and CONFLICT outcomes for the same case.

    Measures how often introducing contradictory evidence
    changes a previously correct answer into a wrong answer.
    """

    grouped = defaultdict(dict)

    for result in results:

        grouped[
            result["case_id"]
        ][
            result["condition"]
        ] = result

    complete_pairs = 0
    clean_correct = 0
    correct_to_wrong = 0
    wrong_to_correct = 0
    unchanged_correct = 0
    unchanged_wrong = 0

    for case_id, conditions in grouped.items():

        if (
            "CLEAN" not in conditions
            or "CONFLICT" not in conditions
        ):
            continue

        complete_pairs += 1

        clean = conditions["CLEAN"]
        conflict = conditions["CONFLICT"]

        clean_is_correct = clean["correct"]
        conflict_is_correct = conflict["correct"]

        if clean_is_correct:
            clean_correct += 1

        if (
            clean_is_correct
            and not conflict_is_correct
        ):
            correct_to_wrong += 1

        elif (
            not clean_is_correct
            and conflict_is_correct
        ):
            wrong_to_correct += 1

        elif (
            clean_is_correct
            and conflict_is_correct
        ):
            unchanged_correct += 1

        else:
            unchanged_wrong += 1

    flip_rate = (
        correct_to_wrong / clean_correct
        if clean_correct > 0
        else 0.0
    )

    return {
        "complete_pairs": complete_pairs,
        "clean_correct": clean_correct,
        "correct_to_wrong": correct_to_wrong,
        "wrong_to_correct": wrong_to_correct,
        "unchanged_correct": unchanged_correct,
        "unchanged_wrong": unchanged_wrong,
        "conflict_induced_flip_rate": flip_rate,
    }


if __name__ == "__main__":

    results = load_results(
        "results/mistral_pilot_results.jsonl"
    )

    analysis = paired_conflict_analysis(
        results
    )

    print("=" * 50)
    print("PAIRED CONFLICT ANALYSIS")
    print("=" * 50)

    print(
        f"Complete CLEAN/CONFLICT pairs: "
        f"{analysis['complete_pairs']}"
    )

    print(
        f"CLEAN cases correct: "
        f"{analysis['clean_correct']}"
    )

    print(
        f"Correct -> Wrong: "
        f"{analysis['correct_to_wrong']}"
    )

    print(
        f"Wrong -> Correct: "
        f"{analysis['wrong_to_correct']}"
    )

    print(
        f"Correct -> Correct: "
        f"{analysis['unchanged_correct']}"
    )

    print(
        f"Wrong -> Wrong: "
        f"{analysis['unchanged_wrong']}"
    )

    print()

    print(
        "Conflict-induced flip rate: "
        f"{analysis['conflict_induced_flip_rate']:.3f}"
    )