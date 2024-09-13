from django.utils import timezone
from uuid import uuid4

from django.db import models

from src.django_project.category_app.models import CategoryModel


class GenreModel(models.Model):
    # app_label = "genre_app"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(CategoryModel, related_name="genres")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "genres"
        ordering = ["-created_at"]
