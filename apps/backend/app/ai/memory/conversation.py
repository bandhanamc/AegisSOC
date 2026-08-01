from app.ai.memory.memory_store import MemoryStore


class Conversation:

    def __init__(self):

        self.memory = MemoryStore()

    def user(

        self,

        text

    ):

        self.memory.add(

            "user",

            text

        )

    def assistant(

        self,

        text

    ):

        self.memory.add(

            "assistant",

            text

        )

    def history(self):

        return self.memory.get_history()