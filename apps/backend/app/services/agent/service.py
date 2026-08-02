from app.ai.agent.agent_orchestrator import AgentOrchestrator



class AgentService:


    def __init__(self):

        self.agent=AgentOrchestrator()



    def process(
        self,
        alert
    ):


        return self.agent.run(
            alert
        )