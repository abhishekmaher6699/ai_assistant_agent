from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict


@dataclass
class ModelResponse:
    content: str | None
    tool_calls: list[ToolCall]
    assistant_message: dict


class Model(ABC):

    @abstractmethod
    def generate(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> ModelResponse:
        pass