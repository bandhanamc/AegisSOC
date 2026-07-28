import json


class PromptBuilder:

    @staticmethod
    def build_mitre_prompt(alert, candidates):

        prompt = f"""
You are a Senior Threat Hunter.

You MUST ONLY use the MITRE techniques provided below.

Do NOT invent techniques.

Do NOT use your own MITRE knowledge.

Alert

{alert}

Possible MITRE Techniques

"""

        for technique in candidates:

            prompt += f"""

Technique ID:
{technique["technique_id"]}

Name:
{technique["name"]}

Description:
{technique["description"]}

Detection:
{technique["detection"]}

-----------------------------------------
"""

        prompt += """

Return ONLY valid JSON.

{
    "techniques":[
        {
            "technique_id":"",
            "confidence":"",
            "reasoning":""
        }
    ]
}
"""

        return prompt