from tools.builtin.clock import get_current_time_tool
from tools.builtin.date import get_current_date_tool

TOOLS = [
    get_current_time_tool,
    get_current_date_tool
]


def get_tool_definitions():
    return [tool.definition() for tool in TOOLS]


def get_tool(tool_name: str):
    for tool in TOOLS:
        if tool.name == tool_name:
            return tool

    return None