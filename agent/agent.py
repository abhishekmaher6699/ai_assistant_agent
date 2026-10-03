from agent.runtime import AgentRuntime


def run_agent(state, message: str) -> str:
    runtime = AgentRuntime(state)
    return runtime.run(message)