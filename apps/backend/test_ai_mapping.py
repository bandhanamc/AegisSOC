from app.database.database import SessionLocal
from app.ai.semantic_matcher import SemanticMatcher


db = SessionLocal()


matcher = SemanticMatcher()


result = matcher.search(
    db,
    "SQL injection vulnerability in web application",
    top_k=5
)


for r in result:
    print(r)


db.close()