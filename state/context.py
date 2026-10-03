class ContextManager:
    def __init__(self, max_tokens=2000):
        self.max_tokens = max_tokens

    def estimate_tokens(self, message):
        content = message.get("content") or ""
        return len(content) // 4 + 1

    def get_turn_tokens(self, turn):
        return sum(
            self.estimate_tokens(message)
            for message in turn
        )

    def split_turns(self, messages):
        turns = []
        current_turn = []

        for message in messages:
            if message.get("role") == "user" and current_turn:
                turns.append(current_turn)
                current_turn = []

            current_turn.append(message)

        if current_turn:
            turns.append(current_turn)

        return turns

    def select_recent_turns(self, turns):
        selected = []
        token_count = 0

        for turn in reversed(turns):
            turn_tokens = self.get_turn_tokens(turn)

            # Always keep the newest turn.
            if not selected and turn_tokens > self.max_tokens:
                selected.insert(0, turn)
                break

            if token_count + turn_tokens > self.max_tokens:
                break

            selected.insert(0, turn)
            token_count += turn_tokens

        return selected

    def get_old_turns(self, messages):
        turns = self.split_turns(messages)
        recent_turns = self.select_recent_turns(turns)

        if len(recent_turns) == len(turns):
            return []

        return turns[:-len(recent_turns)]

    def get_context(self, messages, summary=""):
        turns = self.split_turns(messages)
        recent_turns = self.select_recent_turns(turns)

        context = []

        if summary:
            context.append(
                {
                    "role": "system",
                    "content": (
                        "Here is a summary of the earlier conversation. "
                        "Use it as background context:\n\n"
                        f"{summary}"
                    ),
                }
            )

        for turn in recent_turns:
            context.extend(turn)

        return context