from uuid import UUID
from src.django_project.category_app.mappers import CategoryModelMapper
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


class CategoryDjangoRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel):
        self.category_model = category_model

    def save(self, category: Category) -> None:
        model = CategoryModelMapper.to_model(category)
        model.save()

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            model = self.category_model.objects.get(id=id)
            return CategoryModelMapper.to_entity(model)

        except self.category_model.DoesNotExist:
            return None

    def list(self) -> list[Category]:
        models = self.category_model.objects.all()
        return [CategoryModelMapper.to_entity(model) for model in models]

    def update(self, category: Category) -> None:
        model = CategoryModelMapper.to_model(category)

        self.category_model.objects.filter(id=category.id).update(
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()
