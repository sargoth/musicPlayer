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
