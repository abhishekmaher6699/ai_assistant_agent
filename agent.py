import json

from config import MODEL_PROVIDER
from models.factory import get_model

from tools.core.registry import get_tool_definitions
from tools.core.executor import execute_tool

from state.context import ContextManager
from state.summarizer import ConversationSummarizer

from memory.extractor import MemoryExtractor


def run_agent(state, message: str) -> str:

    model = get_model(MODEL_PROVIDER)

    context_manager = ContextManager(max_tokens=100)
    summarizer = ConversationSummarizer(model)
    memory_extractor = MemoryExtractor(model)

    # Remember where this turn starts
    start_index = len(
        state.conversation.get_messages()
    )

    # Add user's message
    state.conversation.add_message(
        {
            "role": "user",
            "content": message,
        }
    )

    while True:

        turns = context_manager.split_turns(
            state.conversation.get_messages()
        )

        recent_turns = context_manager.get_context_turns(
            state.conversation.get_messages()
        )

        recent_start = len(turns) - len(recent_turns)

        old_turns = context_manager.get_unsummarized_old_turns(
            state.conversation.get_messages(),
            state.summary_boundary,
        )

        if old_turns:

            old_messages = []

            for turn in old_turns:
                old_messages.extend(turn)

            state.summary = summarizer.summarize(
                old_messages,
                previous_summary=state.summary,
            )

            state.summary_boundary = recent_start

        messages = context_manager.get_context(
            state.conversation.get_messages(),
            summary=state.summary,
        )

        relevant_memories = state.memory.search(message)
        if relevant_memories:
            memory_text = "\n".join(
                f"- {memory.content}"
                for memory in relevant_memories
            )

            messages.insert(
                0,
                {
                    "role": "system",
                    "content": (
                        "Relevant long-term memories about the user:\n"
                        f"{memory_text}"
                    ),
                },
            )

        print("CONTEXT:", messages)

        response = model.generate(
            messages=messages,
            tools=get_tool_definitions(),
        )

        # No tool call → final response
        if not response.tool_calls:

            state.conversation.add_message(
                {
                    "role": "assistant",
                    "content": response.content,
                }
            )

            # Extract memories ONLY from the current turn
            new_messages = (
                state.conversation.get_messages()[start_index:]
            )

            new_memories = memory_extractor.extract(
                new_messages
            )

            state.memory.add_extracted(
                new_memories
            )

            return response.content

        # Store assistant tool-call message
        state.conversation.add_message(
            response.assistant_message
        )

        # Execute tools
        for tool_call in response.tool_calls:

            tool_name = tool_call.name
            arguments = tool_call.arguments

            print(
                f"[TOOL] {tool_name}({arguments})"
            )

            result = execute_tool(
                tool_name,
                arguments,
            )

            state.conversation.add_message(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )