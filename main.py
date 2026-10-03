from agent import run_agent
from state.agent_state import AgentState
from state.repository.sqlite import SQLiteRepository


def main():
    print("Personal AI Assistant")
    print("Type 'exit' to quit.\n")
    
    repository = SQLiteRepository()
    state = AgentState(repository)
    state.load()

    while True:
        user_input = input("You > ")

        if user_input.lower() == "exit":
            
            # print("\nFULL HISTORY:")
            # print(state.conversation.get_messages())

            state.save()
            
            break

        if user_input.lower() == "/memory":
            print("\nMEMORIES:")

            for memory in state.memory.get_all():
                print(
                    f"- [{memory.category}] {memory.content}"
                )

            print()
            continue

        if user_input.lower().startswith("/plan "):
            message = user_input[6:]

            response = run_agent(
                state,
                message,
                use_planner=True,
            )

            print(f"Assistant > {response}\n")
            continue

        response = run_agent(
            state,
            user_input,
        )

        print(f"Assistant > {response}\n")


if __name__ == "__main__":
    main()