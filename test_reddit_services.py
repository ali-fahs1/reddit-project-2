import sys
import os
import requests
import django
from time import sleep
DJANGO_PROJECT_SRC = r"C:\Users\user\Desktop\projects\reddit_project\reddit-project-2\src"
if DJANGO_PROJECT_SRC not in sys.path:
    sys.path.append(DJANGO_PROJECT_SRC)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfehome.settings")
django.setup()


from helpers import bd
from reddit import services
from snapshots.tasks import perform_reddit_scrape_task,get_run_progress_instance_task
headers = {
        "Authorization": f"Bearer apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352",
        "Content-Type": "application/json",
    }
run_id=bd.perform_scrape_run(
    subreddit_url='https://www.reddit.com/r/Python/',
    max_posts=3,
    # progress_countdown=1,
    dateFrom="2026-09-20",
    dateTo="2026-09-29"
)

dataset_id=run_id.get("defaultDatasetId")
sleep(15)

dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
items_response = requests.get(dataset_url, headers=headers)

items = items_response.json()
print(services.handele_reddit_thread_results(items))