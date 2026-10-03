from config import MODEL_PROVIDER
from models.factory import get_model

from agent.reactive import ReactiveAgent


def run_agent(state, message: str) -> str:

    model = get_model(MODEL_PROVIDER)

    agent = ReactiveAgent(
        model=model,
        state=state,
    )

    return agent.run(message)