from uuid import uuid4
from django.db import models
from django.utils import timezone  # Import correto do timezone

from src.core.cast_member.domain.cast_member_type import CastMemberType

class CastMemberModel(models.Model):
    app_label = "cast_member_app"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=64, choices=[(tag.name, tag.value) for tag in CastMemberType]
    )
    created_at = models.DateTimeField(default=timezone.now)  # Usando timezone.now corretamente

    class Meta:
        db_table = "cast_member"

    def __str__(self):
        return self.name
