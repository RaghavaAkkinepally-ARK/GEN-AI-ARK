from enum import Enum
from typing import Callable
from pydantic import BaseModel, Field


class ToolName(str, Enum):
    crop_lookup = "crop_lookup"
    weather_lookup = "weather_lookup"
    fertilizer_lookup = "fertilizer_lookup"
    disease_lookup = "disease_lookup"
    soil_lookup = "soil_lookup"


class CropLookupInput(BaseModel):
    crop: str = Field(min_length=2, max_length=80)


TOOLS: dict[ToolName, tuple[type[BaseModel], Callable]] = {}


def register_tool(name: ToolName, schema: type[BaseModel], handler: Callable) -> None:
    TOOLS[name] = (schema, handler)


def execute_tool(name: str, raw_input: dict) -> dict:
    try:
        tool_name = ToolName(name)
    except ValueError as exc:
        raise PermissionError("Unauthorized or unknown tool") from exc

    registration = TOOLS.get(tool_name)
    if registration is None:
        raise PermissionError("Tool is not registered")

    schema, handler = registration
    validated = schema.model_validate(raw_input)
    return handler(validated)

