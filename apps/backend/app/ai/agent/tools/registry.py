from app.ai.investigation.investigation_engine import InvestigationEngine
from app.ai.threat_hunting.threat_hunter import ThreatHunter
from app.ai.memory.engine.memory_engine import MemoryEngine
from app.ai.copilot.copilot_engine import CopilotEngine


class AgentToolRegistry:


    def __init__(self):

        self.investigation = InvestigationEngine()
        self.threat_hunter = ThreatHunter()
        self.memory = MemoryEngine()
        self.copilot = CopilotEngine()



    def investigate_mitre(self, alert):

        vulnerability_id = alert.get(
            "vulnerability_id",
            0
        )


        return self.investigation.investigate(
            vulnerability_id
        )



    def threat_hunt(self, alert):

        return self.threat_hunter.hunt(
            alert
        )



    def retrieve_memory(self, alert):

        query = f"""
        Alert Type:
        {alert.get('type')}

        MITRE:
        {alert.get('mitre')}

        Host:
        {alert.get('host')}
        """


        return self.memory.search(
            query
        )



    def generate_response(self, alert, context):

        return self.copilot.analyze(
            alert,
            context
        )