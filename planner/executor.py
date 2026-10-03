from planner.models import StepStatus
from planner.resolver import resolve_arguments

class PlanExecutor:

    def __init__(self, execute_tool, context):
        self.execute_tool = execute_tool
        self.context = context

    def execute(self, plan):

        results = []

        for index, step in enumerate(plan.steps):

            step.status = StepStatus.RUNNING

            try:
                arguments = resolve_arguments(
                    step.arguments,
                    results
                )

                print(
                    f"[PLAN TOOL] "
                    f"{step.tool}({arguments})"
                )

                result = self.execute_tool(
                    step.tool,
                    arguments,
                    self.context
                )

                if not result["success"]:
                    step.status = StepStatus.FAILED
                    step.error = result["error"]

                    return plan

                step.result = result["result"]
                step.status = StepStatus.COMPLETED

                results.append(result["result"])

            except Exception as error:

                step.status = StepStatus.FAILED
                step.error = str(error)

                return plan

        return plan