from app.core.llm.response_parser import ResponseParser

response = """
{
    "techniques":[
        {
            "technique_id":"T1059.001",
            "confidence":"HIGH",
            "reasoning":"PowerShell execution"
        }
    ]
}
"""

print(ResponseParser.parse(response))