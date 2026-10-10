from functools import lru_cache
from django.utils import timezone
from datetime import timedelta
import helpers.bd
from snapshots.tasks import perform_reddit_scrape_task
import ai

from .models import RedditPost,RedditCommunity



def get_valide_reddit_post_fields():
        skip_fields=['id','post_id','url']
        model_field_name=[field.name for field in RedditPost._meta.get_fields()]

        valide_fields=[x for x in model_field_name if x not in skip_fields]
        return valide_fields
      
def handele_reddit_thread_results(reddit_rsults:list=[]):
    
        valide_fields=get_valide_reddit_post_fields()
        ids=[]

        for item in reddit_rsults:
            post_id=item.get('id')
            url=item.get('url')
            if not all([url,post_id]):
                continue
            update_data={k:v for k,v in item.items() if k in valide_fields}
            
            reddit_post_instance,_= RedditPost.objects.update_or_create(
                post_id=post_id,
                url=url,
                defaults=update_data
            )
            ids.append(reddit_post_instance.id)
        return ids
    
    
    
def handle_reddit_community_scrape_automation(reddit_community_instance, created=False, force_scrape=True, verbose=False):
    print("in handle_reddit_community_scrape_automation")
    reddit_community_instance.refresh_from_db()
    url = reddit_community_instance.url
    active = reddit_community_instance.active 
    if not active and not force_scrape:
        return
    trackable = reddit_community_instance.trackable
    if not trackable and not force_scrape:
        return 
    now = timezone.now()
    last_scrape_event = reddit_community_instance.last_scrape_event
    last_event_delta = None
    min_last_event_delta = timedelta(minutes=5)
    if last_scrape_event is not None:
        last_event_delta = now - last_scrape_event
        scrape_ready = last_event_delta > min_last_event_delta
    else:
        scrape_ready = True
    if force_scrape:
        scrape_ready = True
    if verbose:
        print("Ready to scrape",scrape_ready, reddit_community_instance.url)
        print("Was jsut created", created)
    qs = RedditCommunity.objects.filter(pk=reddit_community_instance.pk)
    qs.update(last_scrape_event = timezone.now())
    if scrape_ready and not created:
        if verbose:
            print("Trigger reddit community post scrape update")
        perform_reddit_scrape_task.delay(
            url, 
            max_posts = 5, 
            progress_countdown=300,
            dateFrom="2026-09-01",
            dateTo="2026-09-29"
        )
    if created:
        if verbose:
            print("First pass reddit community run")
            perform_reddit_scrape_task.delay(
                url, 
                max_posts = 5, 
                progress_countdown=300,
                dateFrom="2026-08-01",
                dateTo="2026-09-30"
            )
    if verbose:
        print("---done---\n")




def handle_topic_to_reddit_community(topic_name, verbose=True):
    if verbose:
        print(f" handle_topic_to_reddit_community Researching {topic_name}")
    community_data = ai.perform_get_reddit_communites(topic_name)
    for community in community_data:
        url = community.pop("url")
        if verbose:
            print(url)
        RedditCommunity.objects.update_or_create(
            url = url,
            defaults = community
        )