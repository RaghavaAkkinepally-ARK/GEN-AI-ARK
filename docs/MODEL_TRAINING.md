# Model Training

`scripts/train_qlora.py` supports a configurable decoder model, 4-bit NF4
quantization, LoRA, checkpoint saves and resumed training. It stops rather than
claiming success if no CUDA GPU is available.

Adapter training is external and requires a properly licensed dataset and accepted
base-model license. No adapter or evaluation result is included by default.
