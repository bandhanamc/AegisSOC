"""
Central AI Service Manager

Loads every AI model only once.

All AI modules use this singleton.
"""

from app.ai.semantic_matcher import SemanticMatcher
from app.ai.faiss_search import FaissMitreSearch
from app.ai.copilot.local_llm import LocalLLM
from app.ai.knowledge.knowledge_engine import KnowledgeEngine
from app.ai.memory.conversation import Conversation


class AIServiceManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.matcher = SemanticMatcher()

            cls._instance.search = FaissMitreSearch()

            cls._instance.llm = LocalLLM()

            cls._instance.knowledge = KnowledgeEngine()

            cls._instance.memory = Conversation()

        return cls._instance