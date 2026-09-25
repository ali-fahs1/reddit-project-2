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
from snapshots.models import apifySnapshot
APIFY_SCRAPE_SORT_OPTIONS = ["Today", "This Week", "This Month", "This Year", "All Time"]

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352")




def perform_scrape_run(
    subreddit_name: str,
    max_posts: int = 20,
    raw: bool = False,
    sort_by_time: str = "This Week",
):

    if sort_by_time not in APIFY_SCRAPE_SORT_OPTIONS:
        sort_by_time = "This Month"

    run_input = {
        "subredditName": subreddit_name,
        "maxPosts": max_posts,
        "subredditSort": "top",
        "subredditTimeframe": 'week',
        "scrapeComments": False,
    }
    
    # Start the Actor asynchronously (non-blocking)
    run_info = client.actor("TwqHBuZZPHJxiQrTU").start(run_input=run_input)
    apifySnapshot.objects.create(
        snapshot_id=run_info.get("id"),
        dataset_id=run_info.get("defaultDatasetId"),
        status="unknown"
    )
    if raw:
        return run_info
    print(run_info.get("id"),)
    # Returns the run_id (equivalent to snapshot_id)
    return run_info.get("id")


run_id=perform_scrape_run(subreddit_name="Python",max_posts=1,raw=False,sort_by_time='week')

def get_run_progress(run_id: str, raw: bool = False):

    # Fetch current execution details
    run_data = client.run(run_id).get()

    apifySnapshot.objects.update_or_create(
            snapshot_id=run_data.get("id"),
            dataset_id=run_data.get("defaultDatasetId"),
 
            defaults={
                'status':run_data.get("status")
            } 
         )
    status = run_data.get("status")
    print(status)
    return status == "SUCCEEDED"
get_run_progress(run_id)