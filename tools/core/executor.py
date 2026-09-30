from tools.core.registry import get_tool


def execute_tool(tool_name: str, arguments: dict):
    tool = get_tool(tool_name)

    if tool is None:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
        }

    try:

        result =  tool.function(**arguments)

        return {
            "success": True,
            "result": result,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }