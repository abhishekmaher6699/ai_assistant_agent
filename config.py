import os

from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")

if MODEL_PROVIDER == "groq" and not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set")