from app.ai.semantic_matcher import SemanticMatcher

matcher = SemanticMatcher()

query = "SQL Injection vulnerability"

candidates = [
    "Cross Site Scripting",
    "SQL Injection attack",
    "Weak Password Policy",
    "Remote Code Execution",
    "SQL Injection detected in login page",
]

print()

results = matcher.search(query, candidates)

for candidate, score in results:
    print(f"{score:.4f}  {candidate}")