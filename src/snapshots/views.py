import json
import helpers.bd
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
from .tasks import get_run_progress_instance_task
# from reddit import services as reddit_db_services

from .models import apifySnapshot
from .tasks import get_run_progress_instance_task
from helpers import bd
from reddit import services as reddit_db_services

APIFY_WEBHOOK_HANDLER__SECRET_KEY = settings.APIFY_WEBHOOK_HANDLER__SECRET_KEY

def download_data(dataset_id):
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    
    headers = {
        "Authorization": f"Bearer apify_api_fegLn4LkdqUz3HUveHc5UUf2au09Wz4df352",
        "Accept": "application/json",
    }

    params = {
        "format": "json",      # Options: json, csv, xlsx, xml
        "clean": "true",       # Excludes hidden fields/metadata
        "limit": 1000,         # Maximum items to fetch per request
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    # Returns the list of scraped items
    return response.json()  

@csrf_exempt
def reddit_post_webhook_handler(request):
    print("in reddit_post_webhook_handler")


    if request.method != "POST":
        return HttpResponse("OK")
    auth=request.headers.get('web_hook_Authorization')
    if auth.startswith("Basic "):
        token=auth.split(" ")[1]
        if token==APIFY_WEBHOOK_HANDLER__SECRET_KEY:
           data=[]
           try:
               data=json.loads(request.body.decode('utf-8'))
               dataset_id=data.get("dataset_id")
               data=download_data(dataset_id)
               

           except:
               pass
           pass
           reddit_db_services.handele_reddit_thread_results(reddit_rsults=data)
    return HttpResponse("OK")


@csrf_exempt
def snapshot_webhook_handler(request):
    print("in snapshot_webhook_handler")
    if request.method != "POST":
        return HttpResponse("OK")
    auth=request.headers.get('web_hook_Authorization')
    if auth.startswith("Basic "):
        token=auth.split(" ")[1]
        if token==APIFY_WEBHOOK_HANDLER__SECRET_KEY:
           data={}
           try:
               data=json.loads(request.body.decode('utf-8'))
           except:
               pass
           snapshot_id=data.get("snapshot_id")
           dataset_id=data.get("dataset_id")
           if snapshot_id:
                qs=apifySnapshot.objects.filter(
                    snapshot_id=snapshot_id,
                    dataset_id=dataset_id )     
                if not qs.exists():
                 instance=apifySnapshot.objects.create(
                    snapshot_id=snapshot_id,
                    dataset_id=dataset_id)    
                 get_run_progress_instance_task(instance.id)
 
                else:
                    instance_ids=qs.values_list("id",flat=True)
                    
                    for instance_id in instance_ids:
                        get_run_progress_instance_task(instance_id)

    return HttpResponse("OK")

    
