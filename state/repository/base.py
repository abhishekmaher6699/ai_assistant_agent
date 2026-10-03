from abc import ABC, abstractmethod

class StateRepository(ABC):

    @abstractmethod
    def save_messages(self, messages: list[dict]):
        pass

    @abstractmethod
    def load_messages(self) -> list[dict]:
        pass

    @abstractmethod
    def save_metadata(self, summary: str, summary_boundary: int):
        pass

    @abstractmethod
    def load_metadata(self) -> tuple[str, int]:
        pass