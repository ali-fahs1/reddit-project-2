from django.db.models.signals import post_save
from  snapshots.tasks import perform_reddit_scrape_task 
from .models import RedditCommunity 
from . import services
def reddit_community_post_save_receiver(sender , instance,created,*args,**kwargs):
    services.handle_reddit_community_scrape_automation(instance,created=created,force_scrape=True,verbose=True)

 
    
post_save.connect(reddit_community_post_save_receiver,sender=RedditCommunity)