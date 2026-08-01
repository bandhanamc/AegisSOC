from app.database.database import SessionLocal

from app.ai.knowledge.knowledge_engine import (
    KnowledgeEngine
)

db = SessionLocal()

engine = KnowledgeEngine()

context = engine.get_context(
    db,
    1102
)

print(context.keys())

print()

print(context["vulnerability"].title)

print()

print(context["asset"].hostname)

print()

print(len(context["mitre"]))

db.close()