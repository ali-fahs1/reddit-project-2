from django.contrib import admin
from .models import RedditCommunity, RedditPost

# Register your models directly
admin.site.register(RedditCommunity)
admin.site.register(RedditPost)