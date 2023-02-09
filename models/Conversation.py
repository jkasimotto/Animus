
class Conversation:

    def __init__(self, messages) -> None:
        self.messages = messages
    
    @property
    def formatted_conversation(self):
        """
        Get a formatted conversation.
        """
        return "\n".join(self.messages)