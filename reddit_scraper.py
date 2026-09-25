from apify_client import ApifyClient

import os
import sys
import django

# 1. Get the directory where reddit_scraper.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Add the `src` directory to Python's search path
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.append(SRC_DIR)

# 3. Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')

# 4. Initialize Django
django.setup()
from reddit.models import RedditPost

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352")
def perform_scrape_snapshot(subredditName,nb_of_posts):
# Prepare the Actor input
        run_input ={
            "content_analysis": False,
            "forceSortNewForTimeFilteredRuns": False,
            "includeNsfw": False,
            "maxComments": 1,
            "maxPosts": nb_of_posts,
            "maximize_coverage": False,
            "scrapeComments": False,
            "sentiment_analysis": False,
            "strictSearch": False,
            "strictTokenFilter": False,
            "subredditName": subredditName,
            "subredditSort": "top",
            "subredditTimeframe": "all"
        }

        # Run the Actor and wait for it to finish
        run = client.actor("TwqHBuZZPHJxiQrTU").call(run_input=run_input)

        # Fetch and print Actor results from the run's dataset using dot notation (.get or attribute access)
        dataset_id = run.get("defaultDatasetId") if isinstance(run, dict) else run.get("defaultDatasetId") if hasattr(run, "get") else run["defaultDatasetId"] if isinstance(run, dict) else getattr(run, "default_dataset_id", None) or run.get("defaultDatasetId", run.get("default_dataset_id"))

        # Alternatively, the most standard SDK property access:
        dataset_id = run["defaultDatasetId"] if isinstance(run, dict) else run.default_dataset_id


        skip_fields=['id','post_id','url']
        model_field_name=[field.name for field in RedditPost._meta.get_fields()]

        valide_fields=[x for x in model_field_name if x not in skip_fields]

        for item in client.dataset(dataset_id).iterate_items():
            post_id=item.get('id')
            print(post_id)
            url=item.get('url')
            update_data={k:v for k,v in item.items() if k in valide_fields}
            RedditPost.objects.update_or_create(
                post_id=post_id,
                url=url,
                defaults=update_data
            )
            
perform_scrape_snapshot("Python", 1)