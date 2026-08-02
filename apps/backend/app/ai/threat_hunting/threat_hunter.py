from app.core.llm.local_llm import LocalLLM


class ThreatHunter:


    def __init__(self):

        self.llm = LocalLLM()



    def hunt(
        self,
        alert_context: dict
    ):


        prompt = f"""
You are a SOC Threat Hunting AI.

Analyze the alert and provide:

1. Threat hypothesis
2. MITRE ATT&CK mapping
3. Hunting queries
4. IOC suggestions
5. Investigation steps


Alert:

{alert_context}

Generate structured threat hunting report.
"""


        result = self.llm.generate(
            prompt
        )


        return {

            "alert": alert_context,

            "threat_hunting_report": result

        }