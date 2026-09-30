from django.contrib import admin

from tracks.models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
