from typing import List, Dict, Union
import numpy as np
import re


class MitreSemanticEngine:
    """
    Semantic MITRE ATT&CK technique matcher.

    Uses:
    1. Sentence embeddings
    2. Keyword evidence
    3. Technique name matching
    4. Score boosting
    """


    def __init__(self):

        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )



    def convert_to_text(
        self,
        data: Union[str, dict]
    ) -> str:
        """
        Convert alert JSON into searchable text.
        """


        if isinstance(data, str):

            return data



        if isinstance(data, dict):

            parts = []


            for key, value in data.items():

                if isinstance(value, list):

                    parts.append(
                        " ".join(
                            map(str, value)
                        )
                    )

                else:

                    parts.append(
                        str(value)
                    )


            return " ".join(parts)



        return str(data)




    def clean_text(
        self,
        text: str
    ):


        text = text.lower()


        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )


        text = re.sub(
            r"\s+",
            " ",
            text
        )


        return text.strip()




    def build_embedding(
        self,
        text
    ):


        text = self.convert_to_text(
            text
        )


        return self.model.encode(
            text,
            normalize_embeddings=True
        )




    def similarity(
        self,
        a,
        b
    ):


        return float(
            np.dot(a,b)
        )




    def calculate_keyword_score(
        self,
        alert_text,
        technique
    ):
        """
        Calculates meaningful keyword evidence.
        """


        alert_words = set(
            self.clean_text(
                alert_text
            ).split()
        )


        technique_name = self.clean_text(
            technique.get(
                "name",
                ""
            )
        )


        technique_description = self.clean_text(
            technique.get(
                "description",
                ""
            )
        )


        detection = self.clean_text(
            technique.get(
                "detection",
                ""
            )
        )


        technique_words = set(
            (
                technique_name
                +
                " "
                +
                technique_description
                +
                " "
                +
                detection
            ).split()
        )



        # Remove generic security words

        ignored_words = {

            "file",
            "command",
            "system",
            "process",
            "execution",
            "user",
            "data",
            "using",
            "access",
            "run",
            "application"

        }



        technique_words = (
            technique_words -
            ignored_words
        )



        matched_words = (
            alert_words &
            technique_words
        )


        return len(
            matched_words
        )




    def technique_name_match(
        self,
        alert_text,
        technique
    ):


        alert_text = self.clean_text(
            alert_text
        )


        technique_name = self.clean_text(
            technique.get(
                "name",
                ""
            )
        )


        return (
            technique_name in alert_text
        )




    def match(
        self,
        alert_text,
        techniques: List[Dict],
        threshold: float = 0.45
    ):


        alert_text = self.convert_to_text(
            alert_text
        )


        alert_embedding = self.build_embedding(
            alert_text
        )


        results = []



        for technique in techniques:



            content = " ".join(
                [
                    technique.get(
                        "name",
                        ""
                    ),

                    technique.get(
                        "description",
                        ""
                    ),

                    technique.get(
                        "detection",
                        ""
                    )
                ]
            )



            technique_embedding = self.build_embedding(
                content
            )



            semantic_score = self.similarity(
                alert_embedding,
                technique_embedding
            )



            keyword_score = self.calculate_keyword_score(
                alert_text,
                technique
            )



            name_match = self.technique_name_match(
                alert_text,
                technique
            )



            final_score = semantic_score



            # Keyword evidence boost

            if keyword_score >= 3:

                final_score += 0.10


            elif keyword_score == 2:

                final_score += 0.07


            elif keyword_score == 1:

                final_score += 0.03




            # Exact technique name boost

            if name_match:

                final_score += 0.15




            if final_score >= threshold:



                results.append(

                    {

                        "technique_id":
                            technique.get(
                                "technique_id"
                            ),


                        "name":
                            technique.get(
                                "name"
                            ),


                        "semantic_score":
                            round(
                                semantic_score,
                                3
                            ),


                        "keyword_score":
                            keyword_score,


                        "technique_name_match":
                            name_match,


                        "score":
                            round(
                                final_score,
                                3
                            ),


                        "reason":
                            "Semantic similarity with keyword and technique evidence"

                    }

                )



        results.sort(

            key=lambda x:x["score"],

            reverse=True

        )



        print(
            "SEMANTIC MATCH RESULTS:"
        )


        for result in results[:3]:

            print(
                result
            )



        return results[:3]