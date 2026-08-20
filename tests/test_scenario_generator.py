from src.generation.scenario_generator import (
    determine_ground_truth,
    generate_dataset,
)


def test_high_value_pending_escalates():
    result = determine_ground_truth(
        amount=125_000,
        approval_threshold=100_000,
        approval_status="PENDING",
    )
    assert result == "ESCALATE"


def test_high_value_rejected_escalates():
    result = determine_ground_truth(
        amount=125_000,
        approval_threshold=100_000,
        approval_status="REJECTED",
    )
    assert result == "ESCALATE"


def test_high_value_approved_processes():
    result = determine_ground_truth(
        amount=125_000,
        approval_threshold=100_000,
        approval_status="APPROVED",
    )
    assert result == "PROCESS"


def test_low_value_pending_processes():
    result = determine_ground_truth(
        amount=75_000,
        approval_threshold=100_000,
        approval_status="PENDING",
    )
    assert result == "PROCESS"


def test_dataset_size():
    dataset = generate_dataset(num_cases=1000, seed=42)
    assert len(dataset) == 1000


def test_reproducibility():
    dataset_a = generate_dataset(num_cases=100, seed=42)
    dataset_b = generate_dataset(num_cases=100, seed=42)

    assert dataset_a == dataset_b