from src.core.category.domain.category import Category, CategoryId
from src.django_project.category_app.models import CategoryModel


class CategoryModelMapper:
    @staticmethod
    def to_entity(model: CategoryModel) -> Category:
        return Category(
            id=CategoryId(model.id),
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id.value,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )
