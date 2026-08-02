import requests



url="http://127.0.0.1:8000/api/v1/copilot/ask"



payload={

"question":
"Investigate suspicious PowerShell execution",

"context":

{

"host":"qa3app02",

"mitre":"T1059.001",

"alert":
"Suspicious PowerShell Execution"

}

}



response=requests.post(

url,

json=payload

)



print(response.status_code)

print(response.json())