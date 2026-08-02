from app.ai.agent.planner.planner import AgentPlanner

from app.ai.agent.executor.executor import AgentExecutor



class AgentOrchestrator:


    def __init__(self):

        self.planner=AgentPlanner()

        self.executor=AgentExecutor()



    def run(
        self,
        alert
    ):


        plan=self.planner.create_plan(
            alert
        )


        execution=self.executor.execute(
            plan
        )


        return {

            "alert":alert,

            "plan":plan,

            "execution":execution

        }