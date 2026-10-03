import json

from config import MODEL_PROVIDER
from models.factory import get_model

from tools.core.registry import get_tool_definitions
from tools.core.executor import execute_tool
from tools.core.context import ToolContext

from state.context import ContextManager
from state.summarizer import ConversationSummarizer

from memory.extractor import MemoryExtractor

from planner import Planner, PlanValidator, PlanExecutor


def run_agent(
    state,
    message: str,
    use_planner=False,
) -> str:

    model = get_model(MODEL_PROVIDER)

    context_manager = ContextManager(max_tokens=100)

    summarizer = ConversationSummarizer(model)
    memory_extractor = MemoryExtractor(model)

    tool_context = ToolContext(
        repository=state.repository,
    )

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

    # -------------------------
    # Explicit planning mode
    # -------------------------

    if use_planner:

        planner = Planner(model)

        plan = planner.create_plan(
            message,
            get_tool_definitions(),
        )

        validator = PlanValidator()

        validator.validate(
            plan,
            get_tool_definitions(),
        )

        print("\n[PLAN]")

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            print(
                f"{index}. "
                f"{step.tool}({step.arguments})"
            )

        executor = PlanExecutor(
            execute_tool,
            tool_context,
        )

        plan = executor.execute(plan)

        print()

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            print(
                f"[STEP {index}] "
                f"{step.status.value}"
            )

        failed_steps = [
            step
            for step in plan.steps
            if step.status.value == "failed"
        ]

        if failed_steps:

            failed_step = failed_steps[0]

            return (
                f"Plan failed at step "
                f"{plan.steps.index(failed_step) + 1}: "
                f"{failed_step.error}"
            )

        return (
            "Plan completed successfully.\n"
            + "\n".join(
                f"Step {index + 1}: {step.result}"
                for index, step in enumerate(
                    plan.steps
                )
            )
        )

    # -------------------------
    # Normal reactive agent
    # -------------------------

    while True:

        messages = (
            state.conversation.get_messages()
        )

        turns = context_manager.split_turns(
            messages
        )

        recent_turns = (
            context_manager.get_context_turns(
                messages
            )
        )

        recent_start = (
            len(turns) - len(recent_turns)
        )

        old_turns = (
            context_manager
            .get_unsummarized_old_turns(
                messages,
                state.summary_boundary,
            )
        )

        # -------------------------
        # Summarization
        # -------------------------

        if old_turns:

            old_messages = []

            for turn in old_turns:
                old_messages.extend(turn)

            state.summary = (
                summarizer.summarize(
                    old_messages,
                    previous_summary=state.summary,
                )
            )

            state.summary_boundary = (
                recent_start
            )

        # -------------------------
        # Build context
        # -------------------------

        messages = context_manager.get_context(
            messages,
            summary=state.summary,
        )

        # -------------------------
        # Retrieve memories
        # -------------------------

        relevant_memories = (
            state.memory.search(message)
        )

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
                        "Relevant long-term memories "
                        "about the user:\n"
                        f"{memory_text}"
                    ),
                },
            )

        # -------------------------
        # Ask model
        # -------------------------

        response = model.generate(
            messages=messages,
            tools=get_tool_definitions(),
        )

        # -------------------------
        # Final response
        # -------------------------

        if not response.tool_calls:

            state.conversation.add_message(
                {
                    "role": "assistant",
                    "content": response.content,
                }
            )

            # Extract memories only from
            # the current conversation turn.
            new_messages = (
                state.conversation
                .get_messages()[start_index:]
            )

            new_memories = (
                memory_extractor.extract(
                    new_messages
                )
            )

            state.memory.add_extracted(
                new_memories
            )

            return response.content

        # -------------------------
        # Store assistant tool call
        # -------------------------

        state.conversation.add_message(
            response.assistant_message
        )

        # -------------------------
        # Execute tools
        # -------------------------

        for tool_call in response.tool_calls:

            tool_name = tool_call.name
            arguments = tool_call.arguments

            print(
                f"[TOOL] "
                f"{tool_name}({arguments})"
            )

            result = execute_tool(
                tool_name,
                arguments,
                tool_context,
            )

            state.conversation.add_message(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )