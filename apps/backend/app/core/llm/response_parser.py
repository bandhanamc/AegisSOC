import json


class ResponseParser:

    @staticmethod
    def parse(response: str):

        try:
            return json.loads(response)

        except Exception:

            start = response.find("{")
            end = response.rfind("}")

            if start != -1 and end != -1:

                return json.loads(response[start:end + 1])

            raise ValueError("Invalid AI response")