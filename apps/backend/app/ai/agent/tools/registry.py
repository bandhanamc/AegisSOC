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



    def execute(self, tool_name, context):


        if tool_name == "investigate_mitre":

            return self.investigation.investigate(
                context
            )


        elif tool_name == "threat_hunt":

            return self.threat_hunter.hunt(
                context
            )


        elif tool_name == "retrieve_memory":

            return self.memory.search(
                context.get("alert")
            )


        elif tool_name == "generate_response":

            return self.copilot.analyze(
                context
            )


        else:

            return {
                "error": "Unknown tool"
            }