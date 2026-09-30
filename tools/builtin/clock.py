from datetime import datetime
from tools.core.base import Tool


def get_current_time():
    return datetime.now().strftime("%I:%M:%S %p")

get_current_time_tool = Tool(
    name="get_current_time",
    description="Get the current local time.",
    function=get_current_time,
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
)