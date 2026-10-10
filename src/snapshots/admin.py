from django.contrib import admin

# Register your models here.
from .models import apifySnapshot

class BrightDataSnapshotAdmin(admin.ModelAdmin):
    list_display = ['snapshot_id', 'status', 'is_downloadable']
    list_filter = ['status']

admin.site.register(apifySnapshot, BrightDataSnapshotAdmin)