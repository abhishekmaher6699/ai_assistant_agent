from dataclasses import dataclass
from enum import Enum

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PlanStep:
    tool: str
    arguments: dict
    status: StepStatus = StepStatus.PENDING
    result: object = None
    error: str | None = None


@dataclass
class Plan:
    goal: str
    steps: list[PlanStep]