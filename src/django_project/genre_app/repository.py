from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import GenreModel


class GenreDjangoRepository(GenreRepository):
    def __init__(self, genre_model: GenreModel = GenreModel):
        self.genre_model = genre_model

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            model = GenreModel.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            model = self.genre_model.objects.get(id=id)
            return Genre(
                id=model.id,
                name=model.name,
                is_active=model.is_active,
                categories=set(model.categories.values_list("id", flat=True)),
                # categories={category.id for category in model.categories.all()},
            )
        except self.genre_model.DoesNotExist:
            return None

    def list(self) -> list[Genre]:
        models = self.genre_model.objects.all()
        return [
            Genre(
                id=model.id,
                name=model.name,
                is_active=model.is_active,
                categories=set(model.categories.values_list("id", flat=True)),
                # categories={category.id for category in models.categories.all()},
            )
            for model in models
        ]

    def update(self, genre: Genre) -> None:
        try:
            model = self.genre_model.objects.get(pk=genre.id)
        except self.genre_model.DoesNotExist:
            raise None
        with transaction.atomic():
            self.genre_model.objects.filter(pk=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            model.categories.set(genre.categories)

    def delete(self, id: UUID) -> None:
        self.genre_model.objects.filter(pk=id).delete()
