from app.ai.memory.memory_store import MemoryStore

memory = MemoryStore()

memory.add(

    "user",

    "Explain SQL Injection"

)

memory.add(

    "assistant",

    "SQL Injection is ..."

)

memory.add(

    "user",

    "Generate Sigma Rule"

)

for item in memory.get_history():

    print(item)