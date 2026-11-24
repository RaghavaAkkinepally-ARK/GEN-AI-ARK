# Evaluation Report

No model or retrieval experiments have been executed unless a dated result file
exists in `experiments/results/`. This document must contain executed configuration,
dataset revision, metrics and limitations. It must not contain fabricated scores.

## CO1 token comparison

Run:

```powershell
python scripts/run_tokenization_experiment.py
```

The script records estimated character-based token counts in English, Telugu and
Hindi. Provider-native tokenizers should replace this fallback in production
experiments and should be documented alongside provider and model versions.

