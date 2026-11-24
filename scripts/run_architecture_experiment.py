import json
from pathlib import Path

from app.services.experiments import architecture_experiment_rows, decoding_experiment_rows


def main() -> None:
    result = {
        "experiment": "architecture_and_decoding_catalog",
        "executed": False,
        "note": "Catalog only; measured generation requires model execution.",
        "architectures": architecture_experiment_rows(),
        "decoding_configs": decoding_experiment_rows(),
    }
    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "architecture_experiment.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

