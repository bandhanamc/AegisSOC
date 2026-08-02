import os
import json
import requests



class LocalLLM:


    def __init__(self):

        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434"
        )


        self.generate_url = os.getenv(
            "OLLAMA_URL",
            f"{self.base_url}/api/generate"
        )


        self.tags_url = f"{self.base_url}/api/tags"


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
    ) -> str:
        """
        Send prompt to local Ollama model.

        Used by:
        - SOC Copilot
        - Investigation Engine
        - Threat Hunting
        - Agentic AI
        """


        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False

        }



        try:


            response = requests.post(

                self.generate_url,

                json=payload,

                timeout=self.timeout

            )


            response.raise_for_status()



            data = response.json()



            if "response" not in data:

                raise Exception(
                    "Unexpected Ollama response format"
                )



            return data["response"]



        except requests.exceptions.ConnectionError:


            raise Exception(

                "Ollama service unavailable. "
                "Start Ollama before running AegisSOC AI engine."

            )



        except requests.exceptions.Timeout:


            raise Exception(

                "Ollama request timeout."

            )



        except requests.exceptions.HTTPError as e:


            raise Exception(

                f"Ollama HTTP error: {str(e)}"

            )



        except Exception as e:


            raise Exception(

                f"Ollama generation failed: {str(e)}"

            )





    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Compatibility wrapper.

        Required by:
        - Agent Executor
        - Threat Hunter
        - Investigation Engine
        - Correlation Engine
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

        Future use:
        - SOC realtime assistant
        - Analyst chat interface
        """


        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": True

        }



        try:


            response = requests.post(

                self.generate_url,

                json=payload,

                stream=True,

                timeout=self.timeout

            )


            response.raise_for_status()



            for line in response.iter_lines():


                if not line:

                    continue



                data = json.loads(
                    line.decode("utf-8")
                )



                if "response" in data:

                    yield data["response"]



                if data.get("done"):

                    break



        except requests.exceptions.ConnectionError:


            raise Exception(

                "Ollama service unavailable."

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
    ) -> dict:
        """
        Check Ollama availability and model status.
        """


        try:


            response = requests.get(

                self.tags_url,

                timeout=10

            )


            response.raise_for_status()



            models = response.json()



            available_models = []


            for model in models.get(
                "models",
                []
            ):

                available_models.append(
                    model.get("name")
                )



            return {


                "status": "healthy",


                "model": self.model,


                "available_models": available_models


            }



        except requests.exceptions.ConnectionError:


            return {


                "status": "unhealthy",


                "error": "Ollama service not running"


            }



        except Exception as e:


            return {


                "status": "unhealthy",


                "error": str(e)


            }