from state.conversation import Conversation


class AgentState:
    def __init__(self, repository):
        self.repository = repository
        self.conversation = Conversation()
        self.summary = ""
        self.summary_boundary = 0

    def load(self):
        messages = self.repository.load_messages()

        for message in messages:
            self.conversation.add_message(message)

        self.summary, self.summary_boundary = (
            self.repository.load_metadata()
        )

    def save(self):
        self.repository.save_messages(
            self.conversation.get_messages()
        )

        self.repository.save_metadata(
            self.summary,
            self.summary_boundary,
        )