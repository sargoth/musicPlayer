from typing import Any

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from musicPlayer.mixins import InvalidTurboFormMixin
from playlists.forms import PlaylistForm
from playlists.models import Playlist
from tracks.models import Track


class PlaylistCreateView(InvalidTurboFormMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = "playlists/create_playlist.html"
    success_url = reverse_lazy("playlists:list_playlists")


class PlaylistListView(ListView):
    model = Playlist
    template_name = "playlists/list_playlists.html"
    context_object_name = "playlists"
    paginate_by = 10

    def get_queryset(self):
        return Playlist.objects.prefetch_related("tracks").all().order_by("title")


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = "playlists/playlist_detail.html"
    context_object_name = "playlist"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tracks = self.object.tracks.select_related("album", "album__artist").all()
        context["tracks"] = tracks

        return context


class RemoveTrackFromPlaylistView(View):
    def get(self, request, playlist_pk, track_pk):
        playlist = get_object_or_404(Playlist, pk=playlist_pk)
        track = get_object_or_404(Track, pk=track_pk)

        context = {
            "playlist": playlist,
            "track": track
        }

        return render(request, "playlists/remove_track.html", context)

    def post(self, request, playlist_pk, track_pk):
        playlist = get_object_or_404(Playlist, pk=playlist_pk)
        playlist.tracks.remove(track_pk)

        return redirect("playlists:playlist_detail", pk=playlist_pk)


class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = "playlists/delete_playlist.html"
    fields = "__all__"
    success_url = reverse_lazy("playlists:list_playlists")


class PlaylistEditView(InvalidTurboFormMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    context_object_name = "playlist"
    template_name = "playlists/edit_playlist.html"
    success_url = reverse_lazy("playlists:list_playlists")

    def get_success_url(self) -> str:
        return reverse("playlists:playlist_detail", kwargs={"pk": self.object.pk})
