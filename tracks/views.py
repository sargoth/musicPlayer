from django.apps import apps
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from tracks.forms import CreateTrackForm
from tracks.models import Track


def create_track_view(request: HttpRequest) -> HttpResponse:
    album_id = request.GET.get("album")
    Album = apps.get_model("catalog", "Album")
    album = get_object_or_404(Album, pk=album_id)
    form = CreateTrackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        track = form.save(commit=False)
        track.album = album
        track.save()

        return redirect("catalog:album_detail", pk=album.pk)

    context = {
        "form": form,
        "album": album
    }

    return render(request, "tracks/create_track.html", context)


def delete_track_view(request: HttpRequest, pk: int) -> HttpResponse:
    track = get_object_or_404(Track, pk=pk)

    if request.method == "POST":
        album_id = track.album.pk
        track.delete()

        return redirect("catalog:album_detail", pk=album_id)

    context = {
        "track": track,
        "album": track.album
    }

    return render(request, "tracks/delete_track.html", context)
