import json

from groq import Groq

from config import GROQ_API_KEY
from models.base import Model, ModelResponse, ToolCall


class GroqModel(Model):

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "qwen/qwen3.8-27b"

    def generate(self, messages, tools=None):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto" if tools else "none",
            max_tokens=500,
        )

        message = response.choices[0].message

        tool_calls = []

        if message.tool_calls:
            for call in message.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=call.id,
                        name=call.function.name,
                        arguments=json.loads(call.function.arguments),
                    )
                )

        assistant_message = {
            "role": "assistant",
            "content": message.content,
        }

        if message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in message.tool_calls
            ]

        return ModelResponse(
            content=message.content,
            tool_calls=tool_calls,
            assistant_message=assistant_message,
        )