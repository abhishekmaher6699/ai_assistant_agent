import json

from models.base import Model

from tools.core.registry import get_tool_definitions
from tools.core.executor import execute_tool
from tools.core.context import ToolContext

from state.context import ContextManager
from state.summarizer import ConversationSummarizer

from memory.extractor import MemoryExtractor


class ReactiveAgent:

    def __init__(self, model: Model, state):
        self.model = model
        self.state = state
        self.context_manager = ContextManager(max_tokens=100)
        self.summarizer = ConversationSummarizer(model)
        self.memory_extractor = MemoryExtractor(model)
        self.tool_context = ToolContext(repository=state.repository)


    def run(self, message: str) -> str:

        start_index = len(
            self.state.conversation.get_messages()
        )

        self.state.conversation.add_message(
            {
                "role": "user",
                "content": message,
            }
        )

        while True:

            messages = (
                self.state.conversation
                .get_messages()
            )

            messages = self._build_context(
                messages,
                message,
            )

            response = self.model.generate(
                messages=messages,
                tools=get_tool_definitions(),
            )

            if not response.tool_calls:

                self.state.conversation.add_message(
                    {
                        "role": "assistant",
                        "content": response.content,
                    }
                )

                self._extract_memories(
                    start_index
                )

                return response.content

            self._handle_tool_calls(response)

    def _build_context(
        self,
        messages,
        query,
    ):

        turns = (
            self.context_manager
            .split_turns(messages)
        )

        recent_turns = (
            self.context_manager
            .get_context_turns(messages)
        )

        recent_start = (
            len(turns) - len(recent_turns)
        )

        old_turns = (
            self.context_manager
            .get_unsummarized_old_turns(
                messages,
                self.state.summary_boundary,
            )
        )

        if old_turns:

            old_messages = []

            for turn in old_turns:
                old_messages.extend(turn)

            self.state.summary = (
                self.summarizer.summarize(
                    old_messages,
                    previous_summary=self.state.summary,
                )
            )

            self.state.summary_boundary = (
                recent_start
            )

        context = self.context_manager.get_context(
            messages,
            summary=self.state.summary,
        )

        memories = self.state.memory.search(
            query
        )

        if memories:

            memory_text = "\n".join(
                f"- {memory.content}"
                for memory in memories
            )

            context.insert(
                0,
                {
                    "role": "system",
                    "content": (
                        "Relevant long-term memories "
                        "about the user:\n"
                        f"{memory_text}"
                    ),
                },
            )

        return context

    def _handle_tool_calls(self, response):

        self.state.conversation.add_message(
            response.assistant_message
        )

        for tool_call in response.tool_calls:

            print(
                f"[TOOL] "
                f"{tool_call.name}"
                f"({tool_call.arguments})"
            )

            result = execute_tool(
                tool_call.name,
                tool_call.arguments,
                self.tool_context,
            )

            self.state.conversation.add_message(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    def _extract_memories(self, start_index):

        new_messages = (
            self.state.conversation
            .get_messages()[start_index:]
        )

        new_memories = (
            self.memory_extractor.extract(
                new_messages
            )
        )

        self.state.memory.add_extracted(
            new_memories
        )