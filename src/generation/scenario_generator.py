from dataclasses import asdict, dataclass
import json
import random
from pathlib import Path


@dataclass
class TransactionCase:
    case_id: str
    amount: float
    approval_threshold: float
    approval_status: str
    ground_truth: str


def determine_ground_truth(
    amount: float,
    approval_threshold: float,
    approval_status: str,
) -> str:
    """
    Determine the correct action using authoritative business rules.

    Rule:
    A transaction above the approval threshold must be escalated
    unless it has already been approved.
    """

    if amount > approval_threshold and approval_status != "APPROVED":
        return "ESCALATE"

    return "PROCESS"


def generate_case(case_number: int) -> TransactionCase:
    """
    Generate one randomized transaction case.
    """

    amount = random.randint(10_000, 250_000)

    approval_threshold = random.choice(
        [50_000, 100_000, 150_000]
    )

    approval_status = random.choice(
        ["APPROVED", "PENDING", "REJECTED"]
    )

    ground_truth = determine_ground_truth(
        amount=amount,
        approval_threshold=approval_threshold,
        approval_status=approval_status,
    )

    return TransactionCase(
        case_id=f"case_{case_number:04d}",
        amount=amount,
        approval_threshold=approval_threshold,
        approval_status=approval_status,
        ground_truth=ground_truth,
    )


def generate_dataset(
    num_cases: int,
    seed: int = 42,
) -> list[TransactionCase]:
    """
    Generate a reproducible collection of transaction cases.
    """

    random.seed(seed)

    return [
        generate_case(case_number=i)
        for i in range(1, num_cases + 1)
    ]


def save_dataset(
    cases: list[TransactionCase],
    output_path: str,
) -> None:
    """
    Save the generated dataset in JSONL format.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for case in cases:
            file.write(json.dumps(asdict(case)) + "\n")


if __name__ == "__main__":

    dataset = generate_dataset(
        num_cases=1000,
        seed=42,
    )

    save_dataset(
        cases=dataset,
        output_path="data/synthetic/transactions.jsonl",
    )

    process_count = sum(
        case.ground_truth == "PROCESS"
        for case in dataset
    )

    escalate_count = sum(
        case.ground_truth == "ESCALATE"
        for case in dataset
    )

    print(f"Generated cases: {len(dataset)}")
    print(f"PROCESS cases: {process_count}")
    print(f"ESCALATE cases: {escalate_count}")
    print("Saved to: data/synthetic/transactions.jsonl")