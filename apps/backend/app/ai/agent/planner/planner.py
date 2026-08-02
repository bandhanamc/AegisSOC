class AgentPlanner:


    def create_plan(
        self,
        alert
    ):


        plan=[]


        if alert.get("mitre"):

            plan.append(
                "investigate_mitre"
            )


        if "PowerShell" in alert.get(
            "type",
            ""
        ):

            plan.append(
                "threat_hunt"
            )


        plan.append(
            "retrieve_memory"
        )


        plan.append(
            "generate_response"
        )


        return plan