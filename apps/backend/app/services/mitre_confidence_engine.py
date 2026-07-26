class MitreConfidenceEngine:
    """
    Calculates final MITRE mapping confidence.
    """


    def calculate(
        self,
        keyword_score: float,
        semantic_score: float
    ):


        final_score = (
            keyword_score * 0.4
            +
            semantic_score * 0.6
        )


        if final_score >= 0.85:
            return {
                "level":"HIGH",
                "score":final_score
            }


        elif final_score >=0.60:
            return {
                "level":"MEDIUM",
                "score":final_score
            }


        else:
            return {
                "level":"LOW",
                "score":final_score
            }