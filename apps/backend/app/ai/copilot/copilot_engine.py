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



    def analyze(
        self,
        alert: dict,
        context: dict
    ):

        """
        Agent execution interface.

        Used by Agentic AI orchestrator
        during automated investigation.
        """


        prompt = f"""

You are an Autonomous SOC Analyst AI Agent.

Perform security analysis on the following alert.


Alert:

{alert}


Additional Investigation Context:

{context}



Generate a professional SOC response containing:


1. Incident Summary

2. Threat Analysis

3. MITRE ATT&CK Mapping

4. Risk Assessment

5. Investigation Findings

6. Recommended Containment Actions

7. Detection Improvement Suggestions


Response should be actionable for SOC analysts.


"""


        response = self.llm.generate(
            prompt
        )


        return {

            "alert": alert,

            "analysis": response,

            "context": context

        }