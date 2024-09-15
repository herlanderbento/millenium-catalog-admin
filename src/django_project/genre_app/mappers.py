from dataclasses import dataclass
from typing import List, Tuple
from src.core.category.domain.category import CategoryId
from src.core.genre.domain.genre import Genre, GenreId
from src.django_project.genre_app.models import GenreModel


@dataclass
class GenreRelations:
    categories_ids: List[str]


class GenreModelMapper:
    @staticmethod
    def to_model(entity: Genre) -> Tuple["GenreModel", GenreRelations]:
        return GenreModel(
            id=entity.id.value,
            name=entity.name,
            created_at=entity.created_at,
        ), GenreRelations(
            categories_ids=[str(category_id) for category_id in entity.categories_id]
        )

    @staticmethod
    def to_entity(model: GenreModel) -> Genre:
        return Genre(
            id=GenreId(model.id),
            name=model.name,
            categories_id={
                CategoryId(category.id) for category in model.categories.all()
            },
            created_at=model.created_at,
        )
