class MitreConfidenceEngine:
    """
    Calculates confidence score for MITRE ATT&CK mappings.

    Scoring priority:

    1. Exact MITRE technique match
    2. Keyword evidence
    3. Semantic similarity

    Confidence Levels:

    HIGH:
        Strong evidence and direct technique identification

    MEDIUM:
        Strong behavioral similarity but no exact name match

    LOW:
        Weak similarity
    """



    def calculate(
        self,
        semantic_score: float,
        keyword_score: int,
        technique_name_match: bool
    ):


        score = 0



        # ---------------------------------
        # Exact technique name match
        # ---------------------------------

        if technique_name_match:

            score += 45



        # ---------------------------------
        # Keyword evidence
        # ---------------------------------

        if keyword_score >= 4:

            score += 30


        elif keyword_score == 3:

            score += 25


        elif keyword_score == 2:

            score += 20


        elif keyword_score == 1:

            score += 10



        # ---------------------------------
        # Semantic similarity
        # ---------------------------------

        if semantic_score >= 0.70:

            score += 25


        elif semantic_score >= 0.55:

            score += 20


        elif semantic_score >= 0.45:

            score += 15


        elif semantic_score >= 0.35:

            score += 10



        # ---------------------------------
        # Behavioral detection boost
        #
        # Example:
        #
        # Alert:
        # encoded command
        #
        # Technique:
        # Command Obfuscation
        #
        # ---------------------------------

        if (
            not technique_name_match
            and
            keyword_score >= 2
            and
            semantic_score >= 0.40
        ):

            score += 20



        # ---------------------------------
        # Exact technique confidence boost
        #
        # Example:
        # powershell.exe -> PowerShell
        #
        # ---------------------------------

        if (
            technique_name_match
            and
            keyword_score >= 2
        ):

            score += 10



        # Limit maximum score

        if score > 100:

            score = 100



        # Debug

        print(
            "CONFIDENCE DEBUG:",
            {
                "semantic_score": semantic_score,
                "keyword_score": keyword_score,
                "technique_name_match": technique_name_match,
                "final_score": score
            }
        )



        # Classification

        if score >= 80:

            return "HIGH"


        elif score >= 50:

            return "MEDIUM"


        else:

            return "LOW"