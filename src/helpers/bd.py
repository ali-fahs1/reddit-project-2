
import requests
from apify_client import ApifyClient
from django.conf import settings
from django.apps import apps
APIFY_ACTOR_ID = "TwqHBuZZPHjxiQrTU"  # Your Reddit Scraper Actor ID



BRIGHT_DATA_DATASET_ID="gd_lvz8ah06191smkebj4"
APIFY_SCRAPE_SORT_OPTIONS = ["Today", "This Week", "This Month", "This Year", "All Time"]


def get_apify_client():
    return ApifyClient(settings.APIFY_API_KEY)


client = ApifyClient("apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352")




def perform_scrape_run(
    subreddit_name: str,
    max_posts: int = 20,
    raw: bool = True,
):


    run_input = {
        "subredditName": subreddit_name,
        "maxPosts": max_posts,
        "subredditSort": "top",
        "subredditTimeframe": 'week',
        "scrapeComments": False,
    }
    
    run_info = client.actor("TwqHBuZZPHJxiQrTU").start(run_input=run_input)
    if raw:
        return run_info
    return run_info.id


run_id=perform_scrape_run(subreddit_name="Python",max_posts=1,raw=False)

def get_run_progress(run_id: str, raw: bool = False):
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')

    # Fetch current execution details
    data = client.run(run_id).get()

    if raw:
        return data
    status = getattr(data, "status", None)
    return status == "SUCCEEDED"


get_run_progress(run_id)  

def download_run_dataset(run_id: str) -> list:
    client =get_apify_client()

    # Get default dataset ID associated with the run
    run_data = client.run(run_id).get()
    dataset_id = run_data.get("defaultDatasetId")

    # Fetch items from dataset
    items = client.dataset(dataset_id).list_items().items
    return items