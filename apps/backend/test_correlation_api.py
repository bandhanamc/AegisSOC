import requests



payload = {


    "alerts":[

        {
            "name":
            "Suspicious PowerShell Execution",

            "technique":
            "T1059.001"
        },


        {
            "name":
            "Credential Dumping",

            "technique":
            "T1003"
        }

    ]

}



response = requests.post(

    "http://127.0.0.1:8000/api/v1/correlation/analyze",

    json=payload

)



print(response.status_code)

print(response.json())