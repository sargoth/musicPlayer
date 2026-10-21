import os
from django.core.exceptions import ValidationError

VALID_EXTENSIONS = [".mp3", ".wav", ".flac", ".aac"]


def validate_url_extension(url: str) -> None:
    if not url:
        return

    main_part, extension = os.path.splitext(url)

    if extension.lower() not in VALID_EXTENSIONS:
        raise ValidationError(
            f"Please provide a supported audio format. "
            f"The allowed valid extensions are {', '.join(VALID_EXTENSIONS)}"
        )


def validate_audio_file(file):
    extension = os.path.splitext(file.name)[1].lower()

    if extension not in VALID_EXTENSIONS:
        raise ValidationError(
            f"File format not supported. Please use one of the following: {', '.join(VALID_EXTENSIONS)}"
        )

    max_file_size_mb = 50

    if file.size > max_file_size_mb * 1024 * 1024:
        raise ValidationError(
            f"File size exceeds the allowed maximum of {max_file_size_mb}. The current file size is {file.size / (1024 * 1024):.1f}MB."
        )