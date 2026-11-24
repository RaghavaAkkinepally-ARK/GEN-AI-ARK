import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def main() -> None:
    training = [
        ("what is irrigation for rice", "rag"),
        ("identify wheat leaf disease", "rag"),
        ("give fertilizer guidance", "rag"),
        ("hello", "prompting"),
        ("summarize my question", "prompting"),
        ("adapt agricultural advice", "qlora"),
    ]
    texts = [row[0] for row in training]
    labels = [row[1] for row in training]
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(texts)
    model = LogisticRegression(max_iter=500).fit(features, labels)

    output = Path("models/router")
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, output / "vectorizer.joblib")
    joblib.dump(model, output / "classifier.joblib")
    (output / "training_manifest.json").write_text(
        json.dumps({"status": "demo-trained", "training_rows": len(training)}, indent=2),
        encoding="utf-8",
    )
    print("Demo router artifacts saved. Replace with held-out experiment data before production.")


if __name__ == "__main__":
    main()

