from functools import lru_cache

from langchain_community.tools.google_serper.tool import GoogleSerperResults
from django.conf import settings

def get_serp_tool(): 
   return GoogleSerperResults(serper_api_key=settings.SERPER_API_KEY)

reddit_tools=[get_serp_tool()]