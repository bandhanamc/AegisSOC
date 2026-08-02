from app.ai.agent.tools.registry import AgentToolRegistry



class AgentExecutor:


    def __init__(self):

        self.tools = AgentToolRegistry()



    def execute_plan(
        self,
        plan,
        context
    ):

        results = {}


        for step in plan:

            try:

                results[step] = self.tools.execute(
                    step,
                    context
                )


            except Exception as e:

                results[step] = {
                    "error": str(e)
                }


        return results