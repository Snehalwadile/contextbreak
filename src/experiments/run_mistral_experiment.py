import json
import time
from collections import defaultdict
from pathlib import Path

from src.evaluation.evaluator import (
    accuracy_by_condition,
    evaluate_case,
    load_cases,
)

from src.evaluation.metrics import (
    conflict_sensitivity,
)

from src.models.mistral_client import (
    run_mistral,
)


RESULTS_PATH = Path(
    "results/mistral_pilot_results.jsonl"
)

NUM_BASE_CASES = 30

MAX_RETRIES = 5


def select_pilot_cases(
    cases: list[dict],
    num_base_cases: int,
) -> list[dict]:
    """
    Select complete CLEAN / CONFLICT / NEUTRAL groups.
    """

    grouped = defaultdict(list)

    for case in cases:
        grouped[case["case_id"]].append(case)

    selected = []

    for case_id in sorted(grouped)[:num_base_cases]:
        selected.extend(grouped[case_id])

    return selected


def load_existing_results(
    path: Path,
) -> list[dict]:
    """
    Load results already completed in a previous run.
    """

    if not path.exists():
        return []

    results = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            if line.strip():
                results.append(
                    json.loads(line)
                )

    return results


def save_result(
    result: dict,
    path: Path,
) -> None:
    """
    Immediately append one successful result.

    This prevents completed API calls from being lost
    if the experiment stops later.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(result) + "\n"
        )


def run_with_retry(
    case: dict,
) -> dict:
    """
    Run one Mistral evaluation with exponential backoff.
    """

    for attempt in range(MAX_RETRIES):

        try:
            return evaluate_case(
                case=case,
                model_fn=run_mistral,
            )

        except Exception as error:

            error_text = str(error)

            if "429" not in error_text:
                raise

            if attempt == MAX_RETRIES - 1:
                raise

            wait_seconds = 2 ** (attempt + 1)

            print(
                f"Rate limited. Waiting "
                f"{wait_seconds} seconds..."
            )

            time.sleep(wait_seconds)

    raise RuntimeError(
        "Maximum retry attempts exceeded."
    )


if __name__ == "__main__":

    all_cases = load_cases(
        "data/synthetic/condition_cases.jsonl"
    )

    pilot_cases = select_pilot_cases(
        cases=all_cases,
        num_base_cases=NUM_BASE_CASES,
    )

    existing_results = load_existing_results(
        RESULTS_PATH
    )

    completed = {
        (
            result["case_id"],
            result["condition"],
        )
        for result in existing_results
    }

    results = list(existing_results)

    print(
        f"Target cases: {len(pilot_cases)}"
    )

    print(
        f"Already completed: "
        f"{len(existing_results)}"
    )

    remaining = (
        len(pilot_cases)
        - len(completed)
    )

    print(
        f"Remaining API calls: {remaining}"
    )

    print()

    for index, case in enumerate(
        pilot_cases,
        start=1,
    ):

        key = (
            case["case_id"],
            case["condition"],
        )

        if key in completed:

            print(
                f"[{index}/{len(pilot_cases)}] "
                f"{case['case_id']} | "
                f"{case['condition']} | SKIPPED"
            )

            continue

        try:

            result = run_with_retry(case)

            save_result(
                result=result,
                path=RESULTS_PATH,
            )

            results.append(result)
            completed.add(key)

            print(
                f"[{index}/{len(pilot_cases)}] "
                f"{result['case_id']} | "
                f"{result['condition']} | "
                f"truth={result['ground_truth']} | "
                f"prediction={result['prediction']} | "
                f"correct={result['correct']}"
            )

        except Exception as error:

            print(
                f"[{index}/{len(pilot_cases)}] "
                f"{case['case_id']} | "
                f"{case['condition']} | "
                f"ERROR: {error}"
            )

    print()
    print("=" * 50)
    print("EXPERIMENT SUMMARY")
    print("=" * 50)

    print(
        f"Successful evaluations: "
        f"{len(results)}/{len(pilot_cases)}"
    )

    if results:

        accuracy = accuracy_by_condition(
            results
        )

        print()
        print("Accuracy by condition:")

        for condition in sorted(accuracy):

            print(
                f"{condition}: "
                f"{accuracy[condition]:.3f}"
            )

        if (
            "CLEAN" in accuracy
            and "CONFLICT" in accuracy
        ):

            sensitivity = conflict_sensitivity(
                accuracy
            )

            print()
            print(
                f"Conflict sensitivity: "
                f"{sensitivity:.3f}"
            )

    print()
    print(
        f"Results saved to: {RESULTS_PATH}"
    )