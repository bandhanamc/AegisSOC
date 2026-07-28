from app.core.llm.ollama_client import OllamaClient

client = OllamaClient()

prompt = """
Explain MITRE ATT&CK technique T1059.001.

Return:

Technique Name
Description
Detection
Mitigation
"""

response = client.generate(prompt)

print()
print("=" * 80)
print("OLLAMA RESPONSE")
print("=" * 80)
print(response)
print("=" * 80)