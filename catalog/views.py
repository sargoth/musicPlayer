from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Album, Artist
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

    return render(request, "catalog/home.html", context)

def list_all_artists_view(request: HttpRequest) -> HttpResponse:
    artists = Artist.objects.prefetch_related("genres").all()
    context = {
        "artists": artists
    }

    return render(request, "catalog/list_artists.html", context)


def list_all_albums_view(request: HttpRequest) -> HttpResponse:
    albums = Album.objects.select_related("artist").all()
    context = {
        "albums": albums
    }

    return render(request, "catalog/list_albums.html", context)


def album_details_view(request: HttpRequest, pk: int) -> HttpResponse:
    album = get_object_or_404(Album.objects.select_related("artist"), pk=pk)
    tracks = album.tracks.all()
    context = {
        "album": album,
        "tracks": tracks
    }

    return render(request, "catalog/album_detail.html", context)


def artist_details_view(request: HttpRequest, pk: int) -> HttpResponse:
    artist = get_object_or_404(Artist.objects.prefetch_related("albums"), pk=pk)
    tracks = Track.objects.filter(album__artist=artist)
    context = {
        "artist": artist,
        "tracks": tracks
    }

    return render(request, "catalog/artist_detail.html", context)
