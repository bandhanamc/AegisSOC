from app.ai.threat_hunting.threat_hunter import ThreatHunter


hunter = ThreatHunter()



alert = {


"type":
"Suspicious PowerShell Execution",


"mitre":
"T1059.001",


"host":
"qa3app02"


}



result = hunter.hunt(
    alert
)


print(result)