from django.db import models


class Playlist(models.Model):
    DEFAULT_PLAYLIST_COVER = "https://images.unsplash.com/photo-1637231065247-016aed55c648"

    title = models.CharField(
        max_length=100,
        help_text="Title of the playlist."
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="An option playlist description."
    )

    cover_img_url = models.URLField(
        blank=True,
        help_text="The URL for the playlist cover.",
        default=DEFAULT_PLAYLIST_COVER
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    tracks = models.ManyToManyField(
        to="tracks.Track",
        blank=True,
        related_name="playlists",
        help_text="Choose the tracks to include in the playlist."
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.cover_img_url or not self.cover_img_url.strip():
            self.cover_img_url = self.DEFAULT_PLAYLIST_COVER
        super().save(*args, **kwargs)

    def formatted_total_duration(self) -> str:
        total_duration = sum(track.duration_in_seconds for track in self.tracks.all())
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60
        seconds = total_duration % 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m {seconds}s"
