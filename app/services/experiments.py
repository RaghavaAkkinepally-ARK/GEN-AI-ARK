from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class GenerationConfig:
    temperature: float
    top_k: int | None = None
    top_p: float | None = None
    decoding: str = "greedy"


@dataclass(frozen=True)
class ArchitectureExperiment:
    model_family: str
    pretraining_objective: str
    suited_to_agriculture_advisory: str


ARCHITECTURES = (
    ArchitectureExperiment("encoder-only", "masked language modeling", "classification and retrieval"),
    ArchitectureExperiment("decoder-only", "causal language modeling", "primary text generation"),
    ArchitectureExperiment("encoder-decoder", "sequence-to-sequence", "translation and summarization"),
)


DECODING_CONFIGS = (
    GenerationConfig(0.0, decoding="greedy"),
    GenerationConfig(0.7, top_k=40, decoding="top-k"),
    GenerationConfig(0.7, top_p=0.9, decoding="top-p"),
    GenerationConfig(0.7, top_k=20, top_p=0.9, decoding="top-k-top-p"),
)


def architecture_experiment_rows() -> list[dict]:
    return [asdict(row) for row in ARCHITECTURES]


def decoding_experiment_rows() -> list[dict]:
    return [asdict(row) for row in DECODING_CONFIGS]

