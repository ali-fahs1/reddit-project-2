
import requests
from apify_client import ApifyClient
from django.conf import settings
from django.apps import apps
import time
from datetime import date,timedelta

APIFY_ACTOR_ID = settings.APIFY_ACTOR_ID






def perform_scrape_run(
    subreddit_url: str,
    max_posts,
    raw: bool = True,
    use_webhook= True,
    dateFrom= None ,
    dateTo=None 
):


    url = f"https://api.apify.com/v2/actors/{APIFY_ACTOR_ID}/runs"
    
    # Force Apify to save results to your static dataset
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352'

    }
    if dateFrom==None and dateTo==None:
        today = date.today().isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        dateFrom= today
        dateTo=tomorrow
        
    print(dateFrom,dateTo)
        
    payload = {
            "urls": [
                subreddit_url   
                        ],

        "maxPosts": max_posts,
        "dateFrom":dateFrom,
        "dataTo":dateTo,
    }
    if use_webhook:
        webhook_headers={
            "web_hook_Authorization":"Basic abc"
        }
        headers.update(webhook_headers)
    response = requests.post(url, headers=headers, json=payload)

    if raw:
        return response.json().get("data", {})
    return response.json().get("data", {}).get("id") # Returns the run_id




def get_run_progress(run_id: str, raw: bool = False):
    url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    
    headers = {
        "Authorization": f"Bearer apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    
    
    # Apify returns data wrapped inside a "data" top-level key
    data = response.json().get("data", {})


    
    if raw:
        return data
        
    status = response.json().get("data", {}).get("status")
    return status == "SUCCEEDED"



def download_snapshot(run_id: str) -> list:

    headers = {
        "Authorization": f"Bearer apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352",
        "Content-Type": "application/json",
    }
    # Step 1: Get the run details to find defaultDatasetId
    run_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    run_res = requests.get(run_url, headers=headers)
    run_res.raise_for_status()
    
    dataset_id = run_res.json().get("data", {}).get("defaultDatasetId")
    if not dataset_id:
        return []

    # Step 2: Fetch items from the dataset
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    dataset_res = requests.get(dataset_url, headers=headers)
    dataset_res.raise_for_status()

    # Returns the list of scraped items
    return dataset_res.json()