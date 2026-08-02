import requests



url="http://127.0.0.1:8000/api/v1/memory/store"


payload={

"id":"report001",

"content":
"""
Suspicious PowerShell execution detected on qa3app02.
MITRE technique T1059.001.
Investigation confirmed malicious activity.
"""

}


print(
requests.post(
url,
json=payload
).json()
)



url="http://127.0.0.1:8000/api/v1/memory/search"



payload={

"query":
"PowerShell attack investigation"

}


print(
requests.post(
url,
json=payload
).json()
)