from typing import List


class PromptBuilder:
    """
    Builds prompts for Ollama models.

    All prompts must request STRICT JSON output.
    """

    @staticmethod
    def build_mitre_prompt(alert: str, candidates: List[dict]) -> str:

        candidate_text = ""

        for c in candidates:

            candidate_text += f"""
Technique ID: {c.get("technique_id")}

Technique Name: {c.get("name")}

Tactic: {c.get("tactic", "")}

Description:
{c.get("description", "")}

Detection:
{c.get("detection", "")}

Platforms:
{c.get("platforms", "")}

Data Sources:
{c.get("data_sources", "")}

Semantic Score:
{round(c.get("score", 0), 3)}

----------------------------------------
"""

        return f"""
You are an expert Cyber Security Threat Hunter.

Your job is to map security alerts to the MITRE ATT&CK framework.

Analyze the alert.

ONLY use the candidate techniques below.

Do NOT invent techniques.

Choose every matching technique.

Return STRICT JSON only.

Schema:

{{
    "techniques":[
        {{
            "technique_id":"",
            "confidence":"HIGH",
            "reasoning":""
        }}
    ]
}}

Alert:

{alert}

Candidate Techniques:

{candidate_text}
"""