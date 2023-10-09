from AI.artificial_intelligence import OpenAI


class conversation:
    def __init__(self):
        self.chat: OpenAI = OpenAI()
        self.id = None

    def __str__(self):
        return f"Conversation: {self.id}\nChat: {self.chat}"

    def __repr__(self):
        return f"Conversation: {self.id}\nChat: {self.chat}"
