import csv
import json
from pathlib import Path

from app.services.llm import CharacterTokenCounter


TEXTS = [
    ("english", "What is the recommended irrigation schedule for rice in clay soil?"),
    ("telugu", "బంక మట్టి నేలలో వరికి ఎలాంటి నీటి నిర్వహణ మంచిది?"),
    ("hindi", "काली मिट्टी में धान की सिंचाई का सही तरीका क्या है?"),
]


def main() -> None:
    counter = CharacterTokenCounter()
    output = []
    for language, text in TEXTS:
        output.append({
            "language": language,
            "text": text,
            "character_count": len(text),
            "utf8_byte_count": len(text.encode("utf-8")),
            "estimated_token_count": counter.count(text),
        })

    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "tokenization_comparison.json"
    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    csv_path = output_dir / "tokenization_comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

    print(json.dumps(output, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()

