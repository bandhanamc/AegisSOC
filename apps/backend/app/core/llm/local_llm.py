import requests
import json


class LocalLLM:

    def __init__(self):

        self.url = "http://127.0.0.1:11434/api/generate"

        self.model = "llama3.1"


    def ask(self, prompt: str):
        """
        Send prompt to local Ollama model
        """

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False

        }


        response = requests.post(
            self.url,
            json=payload,
            timeout=300
        )


        response.raise_for_status()

        return response.json()["response"]



    def generate(self, prompt: str):
        """
        Compatibility wrapper.
        Used by AI engines:
        - Threat Hunter
        - Investigation Engine
        - Correlation Engine
        """

        return self.ask(prompt)



    def stream(self, prompt: str):
        """
        Streaming response from Ollama
        """

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": True

        }


        response = requests.post(

            self.url,

            json=payload,

            stream=True,

            timeout=300

        )


        response.raise_for_status()


        for line in response.iter_lines():

            if line:

                data = json.loads(line)


                if "response" in data:

                    yield data["response"]


                if data.get("done"):

                    break