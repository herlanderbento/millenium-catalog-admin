from src.core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryModel


class CategoryModelMapper:
    @staticmethod
    def to_entity(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )

    @staticmethod
    def to_model(entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
        )
