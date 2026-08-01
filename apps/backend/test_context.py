from app.database.database import SessionLocal

from app.ai.rag.context_builder import ContextBuilder

db = SessionLocal()

builder = ContextBuilder()

context = builder.build(db, 1102)

print(context.keys())

print(context["asset"])

print(len(context["mitre"]))

print(len(context["similar"]))

db.close()