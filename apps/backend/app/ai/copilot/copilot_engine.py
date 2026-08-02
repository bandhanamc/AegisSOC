from app.core.llm.local_llm import LocalLLM


class CopilotEngine:


    def __init__(self):

        self.llm = LocalLLM()



    def ask(
        self,
        question: str,
        context: dict
    ):


        prompt = f"""

You are an experienced SOC Analyst AI Assistant.

Analyze the security context below.

Context:

{context}


User Question:

{question}


Provide:

1. Security Analysis
2. Risk Assessment
3. Investigation Steps
4. Recommended Actions
5. Detection Opportunities


Answer professionally for SOC operations.

"""


        response = self.llm.generate(
            prompt
        )


        return {

            "question": question,

            "analysis": response,

            "context": context

        }