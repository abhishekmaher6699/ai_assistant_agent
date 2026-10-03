from tools.core.base import Tool


def calculate(arguments, context):
    expression = arguments["expression"]

    try:
        return eval(
            expression,
            {"__builtins__": {}},
            {},
        )
    except Exception as error:
        raise ValueError(
            f"Invalid expression: {error}"
        )
    


calculate_tool = Tool(
    name="calculate",
    description="Evaluate a mathematical expression.",
    function=calculate,
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A mathematical expression such as 25 * 18",
            }
        },
        "required": ["expression"],
    },
)