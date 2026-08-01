class PromptBuilder:

    def build_vulnerability_prompt(

        self,

        vulnerability,

        mitre,

        cwe=None

    ):

        prompt = f"""
You are an expert SOC Analyst.

Analyze the following vulnerability.

--------------------------------------

Title:
{vulnerability.title}

Severity:
{vulnerability.severity}

CVSS:
{vulnerability.cvss_score}

Description:
{vulnerability.description}

Solution:
{vulnerability.solution}

CWE:
{cwe if cwe else "Unknown"}

Mapped MITRE Techniques:

"""

        for item in mitre:

            prompt += f"""
Technique:
{item['technique_id']}

Name:
{item['name']}

Confidence:
{round(item['score'],3)}
"""

        prompt += """

Provide:

1. Executive Summary

2. Technical Explanation

3. Risk

4. MITRE ATT&CK Analysis

5. Exploitation Scenario

6. Business Impact

7. Remediation

8. Detection Recommendations

9. SOC Analyst Next Steps

"""

        return prompt