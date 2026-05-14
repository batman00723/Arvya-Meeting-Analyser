from backend.config import settings
from langchain_cerebras import ChatCerebras
from langchain_groq import ChatGroq
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.model= ChatCerebras(
            api_key= settings.cerebras_api_key.get_secret_value(),
            model= "llama3.1-8b",
            temperature= 0.0,
            max_tokens= 150
        )
    def invoke(self, messages):
        response= self.model.invoke(messages)
        return response
    
    def get_structured(self, schema, messages):
        structured_model = self.model.with_structured_output(schema)
        return structured_model.invoke(messages)
    
    