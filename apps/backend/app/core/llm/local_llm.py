import os
import json
import requests



class LocalLLM:


    def __init__(self):

        self.url = os.getenv(
            "OLLAMA_URL",
            "http://127.0.0.1:11434/api/generate"
        )


        self.model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.1"
        )


        self.timeout = int(
            os.getenv(
                "OLLAMA_TIMEOUT",
                "300"
            )
        )



    def ask(
        self,
        prompt: str
    ):
        """
        Send prompt to local Ollama model.
        Used for normal AI responses.
        """


        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False

        }


        try:

            response = requests.post(

                self.url,

                json=payload,

                timeout=self.timeout

            )


            response.raise_for_status()



            result = response.json()



            if "response" not in result:

                raise Exception(
                    "Invalid Ollama response format"
                )


            return result["response"]



        except requests.exceptions.ConnectionError:


            raise Exception(

                "Unable to connect to Ollama service. "
                "Make sure Ollama is running."

            )



        except requests.exceptions.Timeout:


            raise Exception(

                "Ollama request timeout exceeded."

            )



        except Exception as e:


            raise Exception(

                f"Ollama generation failed: {str(e)}"

            )



    def generate(
        self,
        prompt: str
    ):
        """
        Compatibility wrapper.

        Used by:
        - Threat Hunting Engine
        - Investigation Engine
        - Correlation Engine
        - Detection Intelligence
        - SOC Copilot
        """


        return self.ask(
            prompt
        )



    def stream(
        self,
        prompt: str
    ):
        """
        Streaming response from Ollama.
        Used for future realtime SOC assistant.
        """


        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": True

        }



        try:


            response = requests.post(

                self.url,

                json=payload,

                stream=True,

                timeout=self.timeout

            )


            response.raise_for_status()



            for line in response.iter_lines():


                if not line:

                    continue



                data = json.loads(
                    line
                )



                if "response" in data:

                    yield data["response"]



                if data.get("done"):

                    break



        except requests.exceptions.ConnectionError:


            raise Exception(

                "Unable to connect to Ollama service."

            )



        except requests.exceptions.Timeout:


            raise Exception(

                "Ollama streaming timeout."

            )



        except Exception as e:


            raise Exception(

                f"Ollama streaming failed: {str(e)}"

            )



    def health_check(
        self
    ):
        """
        Check Ollama availability.
        """


        try:


            response = requests.get(

                "http://127.0.0.1:11434/api/tags",

                timeout=10

            )


            response.raise_for_status()



            return {

                "status": "healthy",

                "model": self.model

            }



        except Exception as e:


            return {

                "status": "unhealthy",

                "error": str(e)

            }