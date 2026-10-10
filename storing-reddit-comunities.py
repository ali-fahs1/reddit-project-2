import sys
import os
import django
from time import sleep
import json
from google import genai

DJANGO_PROJECT_SRC = r"C:\Users\user\Desktop\projects\reddit_project\reddit-project-2\src"
if DJANGO_PROJECT_SRC not in sys.path:
    sys.path.append(DJANGO_PROJECT_SRC)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfehome.settings")
django.setup()


from helpers import bd
from snapshots.tasks import perform_reddit_scrape_task,get_run_progress_instance_task
from reddit.models import RedditCommunity
import ai
from queries import services

# serper_api_key=os.environ.get("SERPAPI_API_KEY")

# import os
# from langchain_community.tools.google_serper.tool import GoogleSerperResults

# # 1. Ensure the correct environment variable key is set
# os.environ["SERPER_API_KEY"] = os.environ.get("SERPAPI_API_KEY")

# # 2. Instantiate the built-in tool that returns JSON results
# serp_tool = GoogleSerperResults(serper_api_key=serper_api_key)

# # Test the tool directly
# # data = serp_tool.run("latest quantum computing news")
# from langchain.chat_models import init_chat_model

# model=init_chat_model("gemini-3.1-flash-lite",model_provider="google-genai",api_key=os.environ.get("GEMINI_API_KEY"))    

# agent_prompt = """
# You are an expert assistant that can search the internet to find the best reddit communities for any given topic.

# You are also an expert at finding niche communites that discuss the same topic. 
# """
# from pydantic import BaseModel, Field

# class RedditCommunitySchema(BaseModel):
#     name: str = Field(description="Formatted name for Reddit")
#     url: str = Field(description="The complete url of the reddit community")b
#     subreddit_slug: str = Field(description="The slug of the subbreddit such as r/python or r/web or r/trending")
#     member_count: int | None = Field(description="Current member count, if available.")

# class RedditCommunitesSchema(BaseModel):
#     communities: list[RedditCommunitySchema] = Field(description="The list of reddit communites")
    
# from langchain.agents import create_agent

# reddit_agent = create_agent(
#     model=model,  
#     tools=[serp_tool],
#     system_prompt=agent_prompt,
#     response_format=RedditCommunitesSchema
# )

# # Run the agent
# results = reddit_agent.invoke(
#     {"messages": [{"role": "user", "content": "python, javascript, django, web"}]},
#     stream_mode="values"
# )

# for subreddit in results["structured_response"].communities:
#     print(subreddit.name, subreddit.url, subreddit.subreddit_slug, subreddit.member_count)
query="i like skiiing"
topics=services.perform_topic_extraction(query)

print(topics)
# topic_names=", ".join([x.get('name') for x in topics])
# for  x in topics:
#     topic_name=x.get("name")
#     print(f'Researching {topic_name}')

#     community_data=ai.perform_get_reddit_communites(topic_name)
#     for community in community_data:
#         url=community.pop("url")
#         print(url)
#         print(community)
#         instance,created=RedditCommunity.objects.update_or_create(
#             url=url,
#             defaults=community
#         ) 
  
