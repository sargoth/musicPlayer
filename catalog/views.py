from typing import Any

from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from catalog.forms import CreateAlbumForm, CreateArtistForm, GenreForm
from musicPlayer.mixins import InvalidTurboFormMixin
from catalog.models import Album, Artist, Genre
from tracks.models import Track


class ArtistListView(ListView):
    model = Artist
    template_name = "catalog/list_artists.html"
    context_object_name = "artists"
    paginate_by = 10

    def get_queryset(self):
        return Artist.objects.prefetch_related("genres").all()


class AlbumListView(ListView):
    model = Album
    template_name = "catalog/list_albums.html"
    context_object_name = "albums"
    paginate_by = 10

    def get_queryset(self):
        return Album.objects.select_related("artist").all()


class AlbumDetailsView(DetailView):
    model = Album
    template_name = "catalog/album_detail.html"
    context_object_name = "album"

    def get_queryset(self):
        return Album.objects.select_related("artist").prefetch_related("tracks")


class ArtistDetailsView(DetailView):
    model = Artist
    template_name = "catalog/artist_detail.html"
    context_object_name = "artist"

    queryset = Artist.objects.prefetch_related("albums")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tracks"] = Track.objects.filter(album__artist=self.object).select_related("album")
        return context


class AlbumCreateView(InvalidTurboFormMixin, CreateView):
    model = Album
    template_name = "catalog/create_album.html"
    form_class = CreateAlbumForm
    success_url = reverse_lazy("catalog:list_albums")


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = "catalog/delete_album.html"
    success_url = reverse_lazy("catalog:list_albums")


class ArtistCreateView(InvalidTurboFormMixin, CreateView):
    model = Artist
    template_name = "catalog/create_artist.html"
    form_class = CreateArtistForm
    success_url = reverse_lazy("catalog:list_artists")


class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = "catalog/delete_artist.html"
    success_url = reverse_lazy("catalog:list_artists")


class AlbumUpdateView(InvalidTurboFormMixin, UpdateView):
    model = Album
    template_name = "catalog/edit_album.html"
    form_class = CreateAlbumForm

    def get_success_url(self) -> str:
        return reverse("catalog:album_detail", kwargs={"pk": self.object.pk})


class ArtistUpdateView(InvalidTurboFormMixin, UpdateView):
    model = Artist
    template_name = "catalog/edit_artist.html"
    form_class = CreateArtistForm

    def get_success_url(self) -> str:
        return reverse("catalog:artist_detail", kwargs={"pk": self.object.pk})


class GenreListView(ListView):
    model = Genre
    template_name = "catalog/list_genre.html"
    context_object_name = "genres"
    paginate_by = 12


class GenreCreateView(InvalidTurboFormMixin, CreateView):
    model = Genre
    template_name = "catalog/create_genre.html"
    form_class = GenreForm
    success_url = reverse_lazy("catalog:list_genres")

    def get_success_url(self) -> str:
        origin_url = self.request.GET.get("next") or self.request.POST.get("next")

        if origin_url:
            return origin_url

        return super().get_success_url()


class GenreDeleteView(DeleteView):
    model = Genre
    template_name = "catalog/delete_genre.html"
    success_url = reverse_lazy("catalog:list_genres")


class SearchView(TemplateView):
    template_name = "catalog/search_result.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q").strip()

        if query:
            context["query"] = query
            context["tracks"] = (
                Track.objects.filter(
                    Q(title__icontains=query) | Q(album__artist__name__icontains=query)
                ).select_related("album", "album__artist")[:10]
            )

            context["albums"] = (
                Album.objects.filter(
                    Q(title__icontains=query) | Q(artist__name__icontains=query)
                ).select_related("artist")[:8]
            )

            context["artists"] = Artist.objects.filter(
                name__icontains=query
            )[:8]

        return context


class GenreDetailView(DetailView):
    model = Genre
    template_name = "catalog/genre_detail.html"
    context_object_name = "genre"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        artists = Artist.objects.filter(genres=self.object).distinct()
        context["artists"] = artists

        return context
