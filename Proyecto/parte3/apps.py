from django.apps import AppConfig


class Parte3Config(AppConfig):
    default_auto_field = (
        "django.db.models.BigAutoField"  # pyright: ignore[reportAssignmentType]
    )
    name = "parte3"
