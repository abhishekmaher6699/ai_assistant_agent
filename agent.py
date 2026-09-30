import json

from config import MODEL_PROVIDER
from models.factory import get_model
from tools.core.registry import get_tool_definitions
from tools.core.executor import execute_tool


def run_agent(message: str) -> str:

    model = get_model(MODEL_PROVIDER)

    messages = [
        {
            "role": "user",
            "content": message,
        }
    ]

    while True:
        response = model.generate(
            messages=messages,
            tools=get_tool_definitions(),
        )

        if not response.tool_calls:
            return response.content

        messages.append(response.assistant_message)

        for tool_call in response.tool_calls:
            tool_name = tool_call.name
            arguments = tool_call.arguments

            print(f"[TOOL] {tool_name}({arguments})")

            result = execute_tool(tool_name, arguments)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )