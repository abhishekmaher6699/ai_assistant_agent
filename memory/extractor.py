import json


class MemoryExtractor:

    def __init__(self, model):
        self.model = model

    def extract(self, messages):
        conversation = "\n".join(
            f"{message['role']}: {message.get('content', '')}"
            for message in messages
            if message.get("content")
        )

        prompt = f"""
                Extract only information that is useful to remember about the user
                for future conversations.

                Good memories:
                - name
                - stable preferences
                - long-term goals
                - ongoing projects
                - important user facts

                Do NOT extract:
                - greetings
                - temporary emotions
                - casual statements
                - information about the assistant
                - questions that were not answered

                Conversation:
                {conversation}

                Return ONLY valid JSON:
                [
                {{
                    "key": "user_name",
                    "content": "Abhishek",
                    "category": "identity"
                }}
                ]

                Use stable keys such as:
                - user_name
                - occupation
                - current_project
                - long_term_goal
                - preference

                If nothing is worth remembering, return [].
                """

        response = self.model.generate(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        try:
            return json.loads(response.content or "[]")
        except json.JSONDecodeError:
            return []