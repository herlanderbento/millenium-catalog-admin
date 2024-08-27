from django.contrib import admin
from src.django_project.genre_app.models import GenreModel


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(GenreModel, GenreAdmin)
