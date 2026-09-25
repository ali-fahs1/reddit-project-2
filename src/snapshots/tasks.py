import helpers.bd
from django.conf import settings
from django.apps import apps
from django_qstash import stashed_task


MAX_progress_check_count=10

@stashed_task
def perform_reddit_scrape_task( subreddit_name: str,max_posts: int = 20):
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')

    data=helpers.bd.perform_scrape_run(subreddit_name,max_posts,raw=True)
    instance=apifySnapshot.objects.create(
            snapshot_id=data.id,
            dataset_id=helpers.bd.BRIGHT_DATA_DATASET_ID,
            status="unknown",
            url=subreddit_name
        )
    get_run_progress_instance_task.apply_async(args=(instance.id,),countdown=300)
    return data.id
@stashed_task
def get_run_progress_instance_task(instance_id):
    print('here')
    apifySnapshot=apps.get_model("snapshots",'apifySnapshot')
    instance=apifySnapshot.objects.get(id=instance_id)
    snapshot_id=instance.snapshot_id
    data=helpers.bd.get_run_progress(snapshot_id,raw=True)
    
    progress_check_count=instance.progress_check_count
    new_progress_check_count=progress_check_count+1
    
    snapshot_id=data.get("snapshot_id")
    dataset_id=data.get("dataset_id")
    status=data.get("status")

    instance.status=status
    instance.progress_check_count=new_progress_check_count+1
    instance.save()
    instance.refresh_from_db()
    progress_complete=instance.progress_compelete
    if not progress_complete and new_progress_check_count<MAX_progress_check_count:
        print("Recheck how our snapshot is doing")
        delay_delta=30*new_progress_check_count
        get_run_progress_instance_task.apply_async(args=(instance_id,),countdown=delay_delta)
        return
    return status == "SUCCEEDED"
