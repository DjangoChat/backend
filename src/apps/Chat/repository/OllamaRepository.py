import requests
from rest_framework.exceptions import ValidationError


class OllamaRepository:

    def __init__(self, model: str, endpoint: str):
        self.model = model
        self.endpoint = endpoint

    def chat(self, messages):
        try:
            response = requests.post(
                url=f"{self.endpoint}/api/chat",
                data={
                    "model": self.model,
                    "messages": messages,
                },
            )
        except:
            raise ValidationError("Something went wront with the api call")
        return response

    def generate(self, prompt):
        try:
            response = requests.post(
                url=f"{self.endpoint}/api/generate",
                data={
                    "model": self.model,
                    "prompt": prompt,
                },
            )
        except:
            raise ValidationError("Something went wront with the api call")
        return response
