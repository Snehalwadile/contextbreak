from src.evaluation.evaluator import (
    accuracy_by_condition,
    evaluate_dataset,
    load_cases,
    save_results,
)

from src.evaluation.metrics import (
    conflict_sensitivity,
)

from src.models.mock_model import (
    run_mock_model,
)

from src.models.conflict_mock_model import (
    run_conflict_mock_model,
)


def run_experiment(
    model_name: str,
    model_fn,
    cases: list[dict],
) -> None:

    results = evaluate_dataset(
        cases=cases,
        model_fn=model_fn,
    )

    save_results(
        results,
        f"results/{model_name}_results.jsonl",
    )

    accuracy = accuracy_by_condition(
        results
    )

    conflict_drop = conflict_sensitivity(
        accuracy
    )

    print("=" * 50)
    print(f"MODEL: {model_name}")
    print("=" * 50)

    print(
        f"Cases evaluated: {len(results)}"
    )

    print()

    print("Accuracy by condition:")

    for condition in sorted(accuracy):
        print(
            f"{condition}: "
            f"{accuracy[condition]:.3f}"
        )

    print()

    print(
        f"Conflict sensitivity: "
        f"{conflict_drop:.3f}"
    )

    print()

    print(
        "Saved to: "
        f"results/{model_name}_results.jsonl"
    )

    print()


if __name__ == "__main__":

    cases = load_cases(
        "data/synthetic/condition_cases.jsonl"
    )

    run_experiment(
        model_name="baseline_mock",
        model_fn=run_mock_model,
        cases=cases,
    )

    run_experiment(
        model_name="conflict_mock",
        model_fn=run_conflict_mock_model,
        cases=cases,
    )