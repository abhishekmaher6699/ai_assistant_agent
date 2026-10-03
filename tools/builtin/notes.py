from tools.core.base import Tool


def create_note(arguments, context):
    title = arguments["title"]
    content = arguments["content"]

    note_id = context.repository.save_note(
        title,
        content,
    )

    return {
        "id": note_id,
        "title": title,
        "content": content,
    }

def list_notes(arguments, context):
    notes = context.repository.load_notes()

    return {
        "notes": notes
    }

create_note_tool = Tool(
    name="create_note",
    description="Create and permanently save a note.",
    function=create_note,
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the note.",
            },
            "content": {
                "type": "string",
                "description": "The content of the note.",
            },
        },
        "required": ["title", "content"],
    },
)

list_notes_tool = Tool(
    name="list_notes",
    description="Retrieve all saved notes.",
    function=list_notes,
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
)