from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    version: str
    name: str
    template: str


PROMPTS = {
    "agriculture_advisory": PromptTemplate(
        version="v1",
        name="agriculture_advisory",
        template=(
            "You are an agricultural information assistant. Use only provided evidence. "
            "If evidence is insufficient, decline. Never invent weather, soil, dosage or "
            "personal farm measurements. Escalate pesticides or chemicals to experts."
        ),
    )
}


def get_prompt(name: str, version: str | None = None) -> PromptTemplate:
    prompt = PROMPTS.get(name)
    if prompt is None:
        raise KeyError(f"Unknown prompt: {name}")
    if version is not None and prompt.version != version:
        raise KeyError(f"Unknown prompt version: {name}@{version}")
    return prompt

