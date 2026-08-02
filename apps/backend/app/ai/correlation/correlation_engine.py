from app.ai.copilot.local_llm import LocalLLM



class CorrelationEngine:


    def __init__(self):

        self.llm = LocalLLM()



    def correlate(
        self,
        alerts: list
    ):


        prompt = f"""

You are a Senior SOC Analyst.

Analyze these security alerts:

{alerts}


Perform alert correlation.

Return:


## Incident Summary

## Attack Timeline

## Related MITRE ATT&CK Techniques

## Possible Threat Actor Behavior

## Risk Assessment

## Recommended Actions


Identify if these alerts belong to the same attack campaign.

"""


        result = self.llm.ask(
            prompt
        )


        return {

            "alert_count":
                len(alerts),

            "correlation_report":
                result

        }