from dataclasses import dataclass
from typing import Callable

@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    parameters: dict

    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }