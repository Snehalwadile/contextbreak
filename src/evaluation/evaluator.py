import json
from collections import defaultdict
from pathlib import Path
from typing import Callable

from src.models.prompt_builder import (
    build_prompt,
    validate_prompt,
)
from src.models.response_parser import parse_response


def load_cases(path: str) -> list[dict]:
    """
    Load experimental cases from JSONL.
    """

    cases = []

    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            cases.append(json.loads(line))

    return cases


def evaluate_case(
    case: dict,
    model_fn: Callable[[str], str],
) -> dict:
    """
    Evaluate one experimental case.
    """

    prompt = build_prompt(case)

    validate_prompt(
        case=case,
        prompt=prompt,
    )

    raw_response = model_fn(prompt)

    prediction = parse_response(
        raw_response
    )

    correct = (
        prediction
        == case["ground_truth"]
    )

    return {
        "case_id": case["case_id"],
        "condition": case["condition"],
        "ground_truth": case["ground_truth"],
        "prediction": prediction,
        "correct": correct,
    }


def evaluate_dataset(
    cases: list[dict],
    model_fn: Callable[[str], str],
) -> list[dict]:
    """
    Evaluate all experimental cases.
    """

    results = []

    for case in cases:
        results.append(
            evaluate_case(
                case=case,
                model_fn=model_fn,
            )
        )

    return results


def accuracy_by_condition(
    results: list[dict],
) -> dict[str, float]:
    """
    Calculate model accuracy for each condition.
    """

    grouped = defaultdict(list)

    for result in results:
        grouped[result["condition"]].append(
            result["correct"]
        )

    return {
        condition: (
            sum(values) / len(values)
        )
        for condition, values
        in grouped.items()
    }


def save_results(
    results: list[dict],
    path: str,
) -> None:
    """
    Save evaluation output as JSONL.
    """

    output_path = Path(path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        for result in results:
            file.write(
                json.dumps(result) + "\n"
            )