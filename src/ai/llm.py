from functools import lru_cache
from langchain.chat_models import init_chat_model
from django.conf import settings



def get_gemini_model():
    return init_chat_model("gemini-3.1-flash-lite",model_provider="google-genai",api_key=settings.GEMINI_API_KEY) 

