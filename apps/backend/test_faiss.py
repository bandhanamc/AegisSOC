from app.ai.faiss_search import FaissMitreSearch


search = FaissMitreSearch()


query = """
SQL injection vulnerability in web application
"""


results = search.search(
    query,
    top_k=5
)


print("\nFAISS MITRE Results")
print("-------------------")


for result in results:

    print(result)