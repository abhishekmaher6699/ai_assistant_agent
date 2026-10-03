class ConversationSummarizer:

    def __init__(self, model):
        self.model = model

    def summarize(self, messages, previous_summary=""):
        if not messages and not previous_summary:
            return ""

        conversation_text = "\n".join(
            f"{message['role']}: {message.get('content', '')}"
            for message in messages
            if message.get("content")
        )

        prompt = f"""
You maintain a compact summary of an ongoing conversation.

Update the existing summary using the new conversation information.

Preserve:
- important facts about the user
- decisions
- ongoing tasks and projects
- preferences relevant to future interactions
- important context
- unresolved questions
- important tool results

Remove:
- greetings
- casual conversation
- repetition
- irrelevant details

Existing summary:
{previous_summary}

New conversation:
{conversation_text}

Return ONLY the updated summary.
"""

        response = self.model.generate(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        return response.content or previous_summary