from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from catalog.models import Album
from tracks.models import Track


def home_view(request: HttpRequest) -> HttpResponse:
    recent_albums = Album.objects.select_related("artist").all()[:4]
    popular_tracks = Track.objects.select_related(
        "album",
        "album__artist"
    ).order_by(
        "-times_played"
    )[:4]

    context = {
        "recent_albums": recent_albums,
        "popular_tracks": popular_tracks
    }

    return render(request, "home.html", context)
