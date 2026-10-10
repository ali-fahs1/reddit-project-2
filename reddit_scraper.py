# from apify_client import ApifyClien
# import requests

# import os
# import sys
# import django

# # 1. Get the directory where reddit_scraper.py lives
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # 2. Add the `src` directory to Python's search path
# SRC_DIR = os.path.join(BASE_DIR, 'src')
# sys.path.append(SRC_DIR)

# # 3. Set the Django settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')

# # 4. Initialize Django
# django.setup()
# from reddit.models import RedditPost

# # Initialize the ApifyClient with your API token
# def perform_scrape_snapshot(subredditName,max_posts): 
#     url = f"https://api.apify.com/v2/actors/{fatihtahta~reddit-scraper-search-fast}/runs"
    
#     # Force Apify to save results to your static dataset
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': 'Bearer apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352'

#     }
    
#     payload = {
#             "urls": [
#                 "https://www.reddit.com/r/Infographics/"
#                         ],

#         "maxPosts": max_posts,
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     print(response)


#     return response.json().get("data", {}) # Returns the run_id
            
# perform_scrape_snapshot("Python", 1)