from app.ai.correlation import CorrelationEngine



alerts = [

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

    },


    {
        "name":
        "Outbound Connection",

        "technique":
        "T1041"

    }

]



engine = CorrelationEngine()


result = engine.correlate(
    alerts
)


print(result)