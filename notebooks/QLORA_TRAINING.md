# QLoRA Training Notebook Replacement Note

The required interactive notebook should be created in Colab from
`scripts/train_qlora.py`. It must:

1. Verify CUDA and record the GPU model and memory.
2. Install `.[training]`.
3. Document the Hugging Face base model and license URL.
4. Use 4-bit NF4 quantization and LoRA.
5. Prepare deduplicated train/validation/test JSONL splits.
6. Set checkpoint and resume paths.
7. Execute only in an environment with sufficient GPU memory.
8. Save `adapters/agriculture-qlora` and `training_manifest.json`.
9. Never commit adapter weights or credentials.

No notebook, GPU or training run is claimed as complete until its logs and manifest exist.

