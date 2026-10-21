import mutagen
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from .validators import validate_url_extension, validate_audio_file


class Track(models.Model):
    title = models.CharField(
        max_length=100,
        help_text="Title of the track/song."
    )

    duration_in_seconds = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, message="The duration must be 1 second or more.")
        ],
        help_text="Automatically calculated once track URL is provided."
    )

    track_url = models.URLField(
        blank=True,
        null=True,
        validators=[validate_url_extension],
        help_text="Link to the track/song you would like to add."
    )

    audio_file = models.FileField(
        upload_to="tracks/audio_files",
        blank=True,
        null=True,
        validators=[validate_audio_file],
        help_text="Upload an audio file."
    )

    times_played = models.PositiveIntegerField(
        editable=False,
        default=0,
        help_text="How many times the track has been played."
    )

    album = models.ForeignKey(
        to="catalog.Album",
        on_delete=models.CASCADE,
        related_name="tracks",
        help_text="Album the track is part of."
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} - {self.album.title}"

    def convert_track_duration(self) -> str:
        hours = self.duration_in_seconds // 3600
        minutes = (self.duration_in_seconds % 3600) // 60
        seconds = self.duration_in_seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"

    def save(self, *args, **kwargs):
        if self.audio_file and not self.duration_in_seconds:
            try:
                audio = mutagen.File(self.audio_file)

                if audio and audio.info.length:
                    self.duration_in_seconds = audio.info.length
            except Exception as e:
                print(f"Unable to calculate track duration from file: {e}")
        
        super().save(*args, **kwargs)

    @property
    def final_url(self):
        if self.audio_file:
            return self.audio_file.url
        return self.track_url
