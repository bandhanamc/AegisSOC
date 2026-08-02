from app.ai.copilot.copilot_engine import CopilotEngine



class CopilotService:


    def __init__(self):

        self.engine = CopilotEngine()



    def chat(
        self,
        question,
        context
    ):


        return self.engine.ask(

            question,

            context

        )