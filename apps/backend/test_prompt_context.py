from app.database.database import SessionLocal

from app.ai.rag.context_builder import ContextBuilder

from app.ai.rag.prompt_context import PromptContext

db = SessionLocal()

context = ContextBuilder().build(db, 1102)

prompt = PromptContext().build(context)

print(prompt)

db.close()