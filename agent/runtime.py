from config import MODEL_PROVIDER
from models.factory import get_model

from agent.reactive import ReactiveAgent
from planner import Planner, PlanValidator, PlanExecutor

from tools.core.registry import get_tool_definitions
from tools.core.executor import execute_tool
from tools.core.context import ToolContext


class AgentRuntime:

    def __init__(self, state):

        self.state = state
        self.model = get_model(MODEL_PROVIDER)

        self.reactive_agent = ReactiveAgent(
            model=self.model,
            state=state,
        )

        self.tool_context = ToolContext(
            repository=state.repository,
        )

    def run(self, message: str) -> str:

        strategy = self.choose_strategy(message)

        if strategy == "plan":
            return self._run_plan(message)

        return self.reactive_agent.run(message)

    def choose_strategy(self, message: str) -> str:


        response_format = {
           "type": "json_object"
        }
            
        response = self.model.generate(
            messages=[
                {
                "role": "system",
                "content": """
                    Decide how to handle the user's request.

                    Choose "reactive" for:
                    - simple requests
                    - questions
                    - tasks that can be handled one tool/action at a time

                    Choose "plan" for:
                    - complex multi-step tasks
                    - tasks with dependencies
                    - tasks requiring a particular sequence of operations

                    Return ONLY valid JSON in this exact format:

                    {
                        "strategy": "reactive"
                    }

                    or:

                    {
                        "strategy": "plan"
                    }
                """
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            response_format=response_format
        )

        strategy = (response.content or "").strip().lower()

        if strategy == "plan":
            return "plan"

        return "reactive"

    def _run_plan(self, message: str) -> str:

        planner = Planner(self.model)

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
            self.tool_context,
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