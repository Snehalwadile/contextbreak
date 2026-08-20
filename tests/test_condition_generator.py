from collections import Counter, defaultdict

from src.generation.condition_generator import (
    build_condition,
    generate_condition_dataset,
)


SAMPLE_CASE = {
    "case_id": "case_test",
    "ground_truth": "ESCALATE",
    "evidence": [
        {
            "source_type": "POLICY",
            "authority": 3,
            "content": "Transactions above $100,000 require approval.",
            "supports": "ESCALATE",
        },
        {
            "source_type": "DATABASE",
            "authority": 3,
            "content": "Amount: $125,000. Approval: PENDING.",
            "supports": "ESCALATE",
        },
        {
            "source_type": "EMAIL",
            "authority": 1,
            "content": "Old email.",
            "supports": "PROCESS",
        },
    ],
}


def test_clean_supports_ground_truth():
    result = build_condition(SAMPLE_CASE, "CLEAN")

    email = result["evidence"][2]

    assert email["supports"] == "ESCALATE"


def test_conflict_opposes_ground_truth():
    result = build_condition(SAMPLE_CASE, "CONFLICT")

    email = result["evidence"][2]

    assert email["supports"] == "PROCESS"


def test_neutral_has_no_direction():
    result = build_condition(SAMPLE_CASE, "NEUTRAL")

    email = result["evidence"][2]

    assert email["supports"] == "NEUTRAL"


def test_ground_truth_never_changes():
    for condition in ["CLEAN", "CONFLICT", "NEUTRAL"]:
        result = build_condition(
            SAMPLE_CASE,
            condition,
        )

        assert (
            result["ground_truth"]
            == SAMPLE_CASE["ground_truth"]
        )


def test_authoritative_evidence_is_identical():
    generated = [
        build_condition(SAMPLE_CASE, condition)
        for condition in [
            "CLEAN",
            "CONFLICT",
            "NEUTRAL",
        ]
    ]

    policies = [
        case["evidence"][0]
        for case in generated
    ]

    databases = [
        case["evidence"][1]
        for case in generated
    ]

    assert policies[0] == policies[1] == policies[2]
    assert databases[0] == databases[1] == databases[2]


def test_balanced_conditions():
    dataset = generate_condition_dataset(
        [SAMPLE_CASE] * 10
    )

    counts = Counter(
        case["condition"]
        for case in dataset
    )

    assert counts["CLEAN"] == 10
    assert counts["CONFLICT"] == 10
    assert counts["NEUTRAL"] == 10


def test_three_conditions_per_case():
    dataset = generate_condition_dataset(
        [SAMPLE_CASE]
    )

    grouped = defaultdict(list)

    for case in dataset:
        grouped[case["case_id"]].append(
            case["condition"]
        )

    assert set(grouped["case_test"]) == {
        "CLEAN",
        "CONFLICT",
        "NEUTRAL",
    }