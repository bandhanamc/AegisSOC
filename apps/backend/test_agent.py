import requests



url="http://127.0.0.1:8000/api/v1/agent/run"



payload={

"type":
"Suspicious PowerShell Execution",

"host":
"qa3app02",

"mitre":
"T1059.001"

}



response=requests.post(

url,

json=payload

)



print(
response.status_code
)


print(
response.json()
)