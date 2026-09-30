from datetime import datetime

from tools.core.base import Tool


def get_current_date():
    return datetime.now().strftime("%A, %B %d, %Y")


get_current_date_tool = Tool(
    name="get_current_date",
    description="Get the current local date.",
    function=get_current_date,
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
)