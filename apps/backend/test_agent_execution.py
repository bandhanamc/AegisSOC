from app.ai.agent.agent_orchestrator import AgentOrchestrator



agent = AgentOrchestrator()



alert = {


"type":"Suspicious PowerShell Execution",

"host":"qa3app02",

"mitre":"T1059.001"

}



result = agent.run(
    alert
)


print(result)