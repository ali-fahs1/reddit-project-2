import helpers.bd
from django.conf import settings
from django.apps import apps
from django_qstash import stashed_task
from datetime import date,timedelta
from django.utils import timezone


MAX_progress_check_count=10

@stashed_task
def perform_reddit_scrape_task( subreddit_url: str,max_posts,progress_countdown:int =300,    dateFrom= None,dateTo=None ):
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')

    data=helpers.bd.perform_scrape_run(subreddit_url=subreddit_url,max_posts=max_posts,dateFrom=dateFrom,dateTo=dateTo,raw=True )
    print(data)
    instance=apifySnapshot.objects.create(
            snapshot_id=data.get('id'),
            dataset_id=data.get("defaultDatasetId"),
            url=subreddit_url
        )
    get_run_progress_instance_task.apply_async(args=(instance.id,),countdown=progress_countdown)

    return data.get('id')
@stashed_task
def get_run_progress_instance_task(instance_id):
    print('here')
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')
    instance=apifySnapshot.objects.get(id=instance_id)
    snapshot_id=instance.snapshot_id
    data=helpers.bd.get_run_progress(snapshot_id,raw=True)
    
    progress_check_count=instance.progress_check_count
    new_progress_check_count=progress_check_count+1
    snapshot_id=data['id']
    dataset_id=data['defaultDatasetId']
    status=data['status']               
    instance.status=status
    instance.progress_check_count=new_progress_check_count
    instance.save()
    instance.refresh_from_db()
    progress_complete=instance.progress_complete
    
    
    if not progress_complete and new_progress_check_count<MAX_progress_check_count:
        print("Recheck how our snapshot is doing")
        delay_delta=30*new_progress_check_count
        get_run_progress_instance_task.apply_async(args=(instance_id,),countdown=delay_delta)
        return 
    return status == "SUCCEEDED"


@stashed_task
def download_snapshot_to_reddit_post(instance_id:int = None):
    from reddit import services as reddit_db_services
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')
    try:
        instance = apifySnapshot.objects.get(id=instance_id)
    except:
        return 
    try:
        reddit_results = helpers.bd.download_snapshot(instance.snapshot_id)
    except:
        return
    reddit_db_services.handele_reddit_thread_results(reddit_results)


@stashed_task
def snapshots_download_sync(download_all_available=True):
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')

    now = timezone.now()
    last_week = now - timedelta(days=8)
    filters = {
        "status": "SUCCEEDED",
    }
    if not download_all_available:
        filters[ "last_result_sync__lte"] = last_week
    qs = apifySnapshot.objects.filter(
            **filters
        ).order_by('-id')
    for idx, instance in enumerate(qs):
        delay_delta = 30 * idx
        download_snapshot_to_reddit_post.apply_async(kwargs = {
            "instance_id": instance.id,
        }, countdown=delay_delta)
    qs.update(last_result_sync=timezone.now())
