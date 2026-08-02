from app.ai.knowledge.knowledge_engine import KnowledgeEngine
from app.ai.copilot.local_llm import LocalLLM
from app.ai.investigation.context import InvestigationContextBuilder


class InvestigationEngine:


    def __init__(self):

        self.knowledge = KnowledgeEngine()

        self.context_builder = InvestigationContextBuilder()

        self.llm = LocalLLM()



    def investigate(
        self,
        db,
        vulnerability_id: int
    ):


        raw_context = self.knowledge.get_context(
            db,
            vulnerability_id
        )


        if raw_context is None:

            return {
                "error":
                    "Vulnerability context not found"
            }


        context = self.context_builder.build(
            raw_context
        )


        prompt = f"""

You are a Senior SOC Incident Response Analyst.

Analyze this security finding.

Security Context:

{context}


Generate a professional SOC investigation report.

Include:

1. Executive Summary

2. Vulnerability Analysis

3. Affected Asset Details

4. MITRE ATT&CK Analysis

5. Attack Scenario

6. Threat Actor Perspective

7. Business Impact

8. Detection Opportunities

9. Containment Actions

10. Eradication Steps

11. Recovery Plan

12. SOC Analyst Recommendations


Rules:

- Use only provided information.
- Do not invent CVEs.
- Do not invent affected systems.
- Provide actionable SOC recommendations.

"""


        report = self.llm.ask(
            prompt
        )


        return {

            "vulnerability_id":
                vulnerability_id,

            "context":
                context,

            "investigation_report":
                report

        }