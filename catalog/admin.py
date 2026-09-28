from django.contrib import admin

from catalog.models import Genre, Artist, Album


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
