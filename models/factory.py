from models.groq import GroqModel
from models.ollama import OllamaModel


def get_model(provider: str):

    if provider == "groq":
        return GroqModel()

    if provider == "ollama":
        return OllamaModel()

    raise ValueError(f"Unknown model provider: {provider}")