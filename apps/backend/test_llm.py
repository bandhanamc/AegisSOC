from app.ai.copilot.local_llm import LocalLLM


llm = LocalLLM()


response = llm.ask(

    "What is SQL Injection?"

)


print(response)