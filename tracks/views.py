import os
from typing import Any

from django.apps import apps
from django.db.models import F
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView, DeleteView

from musicPlayer.mixins import InvalidTurboFormMixin
from tracks.forms import CreateTrackForm
from tracks.models import Track


class TrackCreateView(InvalidTurboFormMixin, CreateView):
    form_class = CreateTrackForm
    template_name = "tracks/create_track.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        Album = apps.get_model("catalog", "Album")
        self.album = get_object_or_404(Album, pk=request.GET.get("album"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        form.instance.album = self.album
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["album"] = self.album

        return context

    def get_success_url(self) -> str:
        return reverse("catalog:album_detail", kwargs={"pk": self.album.pk})


class TrackDeleteView(DeleteView):
    model = Track
    template_name = "tracks/delete_track.html"
    context_object_name = "track"

    queryset = Track.objects.select_related("album")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["album"] = self.object.album
        return context

    def get_success_url(self) -> str:
        return reverse("catalog:album_detail", kwargs={"pk": self.object.album.pk})


def track_times_played_view(request, pk: int) -> HttpResponse:
    track = get_object_or_404(Track, pk=pk)
    Track.objects.filter(pk=track.pk).update(times_played=F("times_played") + 1)

    return HttpResponse(status=204)


# Source - https://stackoverflow.com/a/70979054
class UploadedTrackPlayView(View):
    def get(self, request, pk, *args, **kwargs):
        audio_file = Track.objects.get(pk=pk).audio_file.path

        with open(audio_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'inline;'
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = os.path.getsize(audio_file)
        return response
