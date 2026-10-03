import json

from config import MODEL_PROVIDER
from models.factory import get_model
from tools.core.registry import get_tool_definitions
from tools.core.executor import execute_tool
from state.context import ContextManager
from state.summarizer import ConversationSummarizer


def run_agent(state, message: str) -> str:

    model = get_model(MODEL_PROVIDER)

    context_manager = ContextManager(
        max_tokens=100
    )

    summarizer = ConversationSummarizer(model)

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

        # Update the summary when older conversation exists.
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

        print("CONTEXT:", messages)

        response = model.generate(
            messages=messages,
            tools=get_tool_definitions(),
        )

        if not response.tool_calls:

            state.conversation.add_message(
                {
                    "role": "assistant",
                    "content": response.content,
                }
            )

            return response.content

        # Store the assistant's tool-call message.
        state.conversation.add_message(
            response.assistant_message
        )

        # Execute every tool requested by the model.
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