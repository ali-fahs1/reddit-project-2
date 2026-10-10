import sys
import os
import django
from time import sleep
DJANGO_PROJECT_SRC = r"C:\Users\user\Desktop\projects\reddit_project\reddit-project-2\src"
if DJANGO_PROJECT_SRC not in sys.path:
    sys.path.append(DJANGO_PROJECT_SRC)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfehome.settings")
django.setup()


from helpers import bd
from snapshots.tasks import perform_reddit_scrape_task,get_run_progress_instance_task

run_id=perform_reddit_scrape_task(
    subreddit_url='https://www.reddit.com/r/Python/',
    max_posts=3,
    progress_countdown=1,
    dateFrom="2026-09-20",
    dateTo="2026-09-29"
)

print(run_id)


