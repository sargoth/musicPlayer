from django import template

register = template.Library()

@register.filter
def description_truncate(value: str, max_length: int=200) -> str:
    if not value or not isinstance(value, str) or len(value) <= max_length:
        return value or ""

    truncated = value[:max_length].rsplit(" ", 1)[0]

    return f"{truncated}..."