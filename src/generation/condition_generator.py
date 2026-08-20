import json
from pathlib import Path
from typing import Any


def load_jsonl(path: str) -> list[dict[str, Any]]:
    records = []

    with Path(path).open("r", encoding="utf-8") as file:
        for line in file:
            records.append(json.loads(line))

    return records


def opposite_decision(decision: str) -> str:
    return "PROCESS" if decision == "ESCALATE" else "ESCALATE"


def build_condition(
    case: dict[str, Any],
    condition: str,
) -> dict[str, Any]:

    ground_truth = case["ground_truth"]

    policy = next(
        item for item in case["evidence"]
        if item["source_type"] == "POLICY"
    )

    database = next(
        item for item in case["evidence"]
        if item["source_type"] == "DATABASE"
    )

    if condition == "CLEAN":
        email = {
            "source_type": "EMAIL",
            "authority": 1,
            "content": (
                f"The operations manager reviewed the transaction "
                f"and recommends {ground_truth}."
            ),
            "supports": ground_truth,
        }

    elif condition == "CONFLICT":
        conflicting_decision = opposite_decision(
            ground_truth
        )

        email = {
            "source_type": "EMAIL",
            "authority": 1,
            "content": (
                f"The operations manager reviewed the transaction "
                f"and strongly recommends {conflicting_decision}. "
                f"No further review is necessary."
            ),
            "supports": conflicting_decision,
        }

    elif condition == "NEUTRAL":
        email = {
            "source_type": "EMAIL",
            "authority": 1,
            "content": (
                "The operations manager confirmed receipt of the "
                "transaction and requested normal processing procedures."
            ),
            "supports": "NEUTRAL",
        }

    else:
        raise ValueError(
            f"Unknown condition: {condition}"
        )

    return {
        "case_id": case["case_id"],
        "condition": condition,
        "ground_truth": ground_truth,
        "evidence": [
            policy,
            database,
            email,
        ],
    }


def generate_condition_dataset(
    base_cases: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    conditions = [
        "CLEAN",
        "CONFLICT",
        "NEUTRAL",
    ]

    dataset = []

    for case in base_cases:
        for condition in conditions:
            dataset.append(
                build_condition(
                    case=case,
                    condition=condition,
                )
            )

    return dataset


def save_jsonl(
    records: list[dict[str, Any]],
    path: str,
) -> None:

    output_path = Path(path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        for record in records:
            file.write(
                json.dumps(record) + "\n"
            )


if __name__ == "__main__":

    base_cases = load_jsonl(
        "data/synthetic/evidence_cases.jsonl"
    )

    condition_cases = generate_condition_dataset(
        base_cases
    )

    save_jsonl(
        condition_cases,
        "data/synthetic/condition_cases.jsonl",
    )

    clean_count = sum(
        case["condition"] == "CLEAN"
        for case in condition_cases
    )

    conflict_count = sum(
        case["condition"] == "CONFLICT"
        for case in condition_cases
    )

    neutral_count = sum(
        case["condition"] == "NEUTRAL"
        for case in condition_cases
    )

    print(
        f"Base evidence cases: {len(base_cases)}"
    )
    print(
        f"Total condition cases: "
        f"{len(condition_cases)}"
    )
    print(f"CLEAN: {clean_count}")
    print(f"CONFLICT: {conflict_count}")
    print(f"NEUTRAL: {neutral_count}")
    print(
        "Saved to: "
        "data/synthetic/condition_cases.jsonl"
    )