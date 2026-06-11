import request
import logging
from rest_framework.exceptions import ValidationError


class OllamaRepository:
    logger = logging.getLogger(__name__)

    def __init__(self, model: str, endpoint: str):
        self.model = model
        self.endpoint = endpoint

    def chat(self, messages):
        try:
            response = request.post(
                url=f"{self.endpoint}/api/chat",
                data={
                    "model": self.model,
                    "messages": messages,
                },
            )
            self.logger.info(response)
        except:
            raise ValidationError("Something went wront with the api call")
        return response

    def generate(self, prompt):
        try:
            response = request.post(
                url=f"{self.endpoint}/api/generate",
                data={
                    "model": self.model,
                    "prompt": prompt,
                },
            )
            self.logger.info(response)
        except:
            raise ValidationError("Something went wront with the api call")
        return response
