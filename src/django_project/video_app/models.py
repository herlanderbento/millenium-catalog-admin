from django.utils import timezone
from django.db import models

# Create your models here.
from uuid import uuid4

from django.db import models

from src.core.video.domain.audio_video_media import MediaStatus, Rating
from src.django_project.cast_member_app.models import CastMemberModel
from src.django_project.category_app.models import CategoryModel
from src.django_project.genre_app.models import GenreModel


class VideoModel(models.Model):
    # app_label = "video_app"

    RATING_CHOICES = [(rating.name, rating.value) for rating in Rating]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    launch_year = models.IntegerField()
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    opened = models.BooleanField()
    published = models.BooleanField()
    rating = models.CharField(max_length=255, choices=RATING_CHOICES)

    categories = models.ManyToManyField(CategoryModel, related_name="videos")
    genres = models.ManyToManyField(GenreModel, related_name="videos")
    cast_members = models.ManyToManyField(CastMemberModel, related_name="videos")

    banner = models.OneToOneField(
        "ImageMediaModel", null=True, blank=True, on_delete=models.SET_NULL
    )
    thumbnail = models.OneToOneField(
        "ImageMediaModel",
        null=True,
        blank=True,
        related_name="video_thumbnail",
        on_delete=models.SET_NULL,
    )
    thumbnail_half = models.OneToOneField(
        "ImageMediaModel",
        null=True,
        blank=True,
        related_name="video_thumbnail_half",
        on_delete=models.SET_NULL,
    )
    trailer = models.OneToOneField(
        "AudioVideoMediaModel",
        null=True,
        blank=True,
        related_name="video_trailer",
        on_delete=models.SET_NULL,
    )
    video = models.OneToOneField(
        "AudioVideoMediaModel",
        null=True,
        blank=True,
        related_name="video_media",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "video"
        ordering = ["-created_at"]


class ImageMediaModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)


class AudioVideoMediaModel(models.Model):
    STATUS_CHOICES = [(status.name, status.value) for status in MediaStatus]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    name = models.CharField(max_length=255)
    raw_location = models.CharField(max_length=255)
    encoded_location = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default=MediaStatus.PENDING.value
    )
