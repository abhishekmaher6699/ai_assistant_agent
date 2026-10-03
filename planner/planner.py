import json

from models.base import Model
from planner.models import Plan, PlanStep


class Planner:

    def __init__(self, model: Model):
        self.model = model

    def create_plan(self, goal, tool_definitions):

        prompt = f"""
            Create a plan to accomplish this goal:

            {goal}

            Available tools:
            {json.dumps(tool_definitions, indent=2)}

            Rules:
            - Use only available tools.
            - Use the minimum number of steps.
            - Later steps may reference previous results.
            - Return ONLY valid JSON.

            Format:
            {{
                "steps": [
                    {{
                        "tool": "tool_name",
                        "arguments": {{}}
                    }}
                ]
            }}
            """

        response = self.model.generate(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        content = response.content or ""

        if not content.strip():
            raise ValueError(
                "Planner returned an empty response"
            )

        content = content.strip()

        if content.startswith("```"):
            lines = content.splitlines()

            lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Planner returned invalid JSON: {content}"
            ) from error


        steps = [
            PlanStep(
                tool=step["tool"],
                arguments=step.get("arguments", {}),
            )
            for step in data["steps"]
        ]

        return Plan(
            goal=goal,
            steps=steps,
        )