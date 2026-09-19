import json
from langchain_community.utilities import SerpAPIWrapper


from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os
load_dotenv()


my_SERPAPI_API_KEY= os.environ.get("SERPAPI_API_KEY")

search = SerpAPIWrapper(serpapi_api_key=my_SERPAPI_API_KEY)
result = search.results("reddit hezbollah")
organic = result.get("organic_results", [])
for r in organic:
    print(r.get("title"), "-", r.get("link"))