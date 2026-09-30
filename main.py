from agent import run_agent


def main():
    print("Personal AI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You > ")

        if user_input.lower() == "exit":
            break

        response = run_agent(user_input)

        print(f"Assistant > {response}\n")


if __name__ == "__main__":
    main()