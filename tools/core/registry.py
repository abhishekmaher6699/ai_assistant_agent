from tools.builtin.clock import get_current_time_tool
from tools.builtin.date import get_current_date_tool
from tools.builtin.calculator import calculate_tool
from tools.builtin.notes import create_note_tool, list_notes_tool

TOOLS = [
    get_current_time_tool,
    get_current_date_tool,
    calculate_tool,
    create_note_tool,
    list_notes_tool
]


def get_tool_definitions():
    return [tool.definition() for tool in TOOLS]


def get_tool(tool_name: str):
    for tool in TOOLS:
        if tool.name == tool_name:
            return tool

    return None