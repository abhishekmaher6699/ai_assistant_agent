class PlanValidator:

    def validate(self, plan, tools):

        available_tools = {
            tool["function"]["name"]
            for tool in tools
        }

        if not plan.steps:
            raise ValueError("Plan contains no steps")

        for index, step in enumerate(plan.steps):

            if step.tool not in available_tools:
                raise ValueError(
                    f"Step {index} uses unknown tool: "
                    f"{step.tool}"
                )

            if not isinstance(step.arguments, dict):
                raise ValueError(
                    f"Step {index} arguments must be an object"
                )

        return True