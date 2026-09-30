from agent import run_agent
from state.agent_state import AgentState
from state.repository.sqlite import SQLiteRepository


def main():
    print("Personal AI Assistant")
    print("Type 'exit' to quit.\n")
    
    repository = SQLiteRepository()
    state = AgentState(repository)
    state.laod()

    while True:
        user_input = input("You > ")

        if user_input.lower() == "exit":
            state.save()
            # print(state.conversation.get_messages())
            break

        response = run_agent(
            state,
            user_input,
        )

        print(f"Assistant > {response}\n")


if __name__ == "__main__":
    main()