"""
AI Memory Store

Stores the last AI interactions.

Later this will move to Redis/PostgreSQL.
"""

from collections import deque


class MemoryStore:

    def __init__(self):

        self.history = deque(maxlen=10)

    def add(
        self,
        role,
        message
    ):

        self.history.append({

            "role": role,

            "message": message

        })

    def clear(self):

        self.history.clear()

    def get_history(self):

        return list(self.history)