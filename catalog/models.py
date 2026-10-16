import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from musicPlayer.models import TimeStampModel
from tracks.models import Track


class Genre(models.Model):
    class GenreChoices(models.TextChoices):
        ROCK = "rock", "Rock"
        POP = "pop", "Pop"
        RAP = "rap", "Rap"
        HIP_HOP = "hip_hop", "Hip-Hop"
        ELECTRONIC = "electronic", "Electronic"
        JAZZ = "jazz", "Jazz"
        CLASSICAL = "classical", "Classical"
        R_AND_B = "r_and_b", "R&B"
        INDIE = "indie", "Indie"
        METAL = "metal", "Metal"
        LO_FI = "lo_fi", "Lo-Fi"
        BLUES = "blues", "Blues"
        SOUL = "soul", "Soul"
        COUNTRY = "country", "Country"
        FOLK = "folk", "Folk"
        REGGAE = "reggae", "Reggae"
        PUNK = "punk", "Punk"
        DISCO = "disco", "Disco"
        FUNK = "funk", "Funk"
        HOUSE = "house", "House"
        TECHNO = "techno", "Techno"
        AMBIENT = "ambient", "Ambient"
        SOUNDTRACK = "soundtrack", "Soundtrack"
        LATIN = "latin", "Latin"
        OTHER = "other", "Other"

    name = models.CharField(
        max_length=50,
        choices=GenreChoices.choices,
        unique=True,
        help_text="Enter a unique music genre (eg., Rock, Hip-Hop)."
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Automatically generated URL-friendly identifier."
    )

    class Meta:
        verbose_name_plural = "Genres"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.get_name_display()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Artist(models.Model):
    DEFAULT_ARTIST_IMAGE = "https://images.unsplash.com/photo-1707025204723-27d332fc36ea"

    name = models.CharField(
        max_length=100,
        help_text="Name of artist or band."
    )

    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Optionally, add or paste info about the artist or band here."
    )

    image_url = models.URLField(
        blank=True,
        default=DEFAULT_ARTIST_IMAGE
    )

    genres = models.ManyToManyField(
        to=Genre,
        related_name="artists",
        help_text="Select one or more genres for this artist/band."
    )

    class Meta:
        verbose_name_plural = "Artists"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.image_url or not self.image_url.strip():
            self.image_url = self.DEFAULT_ARTIST_IMAGE
        super().save(*args, **kwargs)


class Album(TimeStampModel):
    DEFAULT_ALBUM_IMAGE = "https://plus.unsplash.com/premium_photo-1682125896993-12a1758b6cb3"

    title = models.CharField(
        max_length=200,
        help_text="Official title of the album"
    )
    release_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1860, message="Release year must be after 1860."),
            MaxValueValidator(datetime.date.today().year, message="Release year cannot be in the future.")
        ],
        help_text="Album release year (eg., 2026)"
    )
    cover_image_url = models.URLField(
        blank=True,
        default=DEFAULT_ALBUM_IMAGE,
        help_text="Album cover artwork URL"
    )
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
        related_name="albums"
    )

    class Meta:
        verbose_name_plural = "Albums"
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.cover_image_url or not self.cover_image_url.strip():
            self.cover_image_url = self.DEFAULT_ALBUM_IMAGE
        super().save(*args, **kwargs)

    def total_duration(self):
        total_track_duration = sum(track.duration_in_seconds for track in self.tracks.all())

        minutes = total_track_duration // 60
        seconds = total_track_duration % 60

        return f"{minutes}:{seconds:02d}"
