import ollama

from models.base import Model, ModelResponse, ToolCall


class OllamaModel(Model):

    def __init__(self):
        self.model = "qwen3:8b"

    def generate(self, messages, tools=None, response_format=None):

        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            format=response_format,
        )

        message = response.message

        tool_calls = []

        if message.tool_calls:
            for index, call in enumerate(message.tool_calls):
                tool_calls.append(
                    ToolCall(
                        id=f"ollama_call_{index}",
                        name=call.function.name,
                        arguments=call.function.arguments,
                    )
                )

        return ModelResponse(
            content=message.content,
            tool_calls=tool_calls,
            assistant_message=message.model_dump(),
        )