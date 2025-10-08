from django.apps import AppConfig


class Parte2Config(AppConfig):
    default_auto_field = (
        "django.db.models.BigAutoField"  # pyright: ignore[reportAssignmentType]
    )
    name = "parte2"
