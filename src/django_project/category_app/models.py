from django.utils import timezone  # Import correto do timezone
from uuid import uuid4
from django.db import models

class CategoryModel(models.Model):
    app_label = "category_app"

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now) 
    class Meta:
        db_table = "categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
