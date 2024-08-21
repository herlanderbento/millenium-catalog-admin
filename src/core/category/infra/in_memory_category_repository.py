from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category] = None):
        self.categories: list[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category:
        # for category in self.categories:
        #     if category.id == id:
        #         return category
        # return None
        return next((c for c in self.categories if c.id == id), None)

    def list(self) -> list[Category]:
        return self.categories[
            :
        ]  # return a copy of the list to prevent mutation of the original list by other code

    def delete(self, id: UUID) -> None:
        # category = self.get_by_id(id)
        # self.categories.remove(category)
        self.categories = [c for c in self.categories if c.id != id]

    def update(self, category: Category) -> None:
        # index = self.categories.index(self.get_by_id(category.id))
        # self.categories[index] = category
        self.categories = [
            c if c.id != category.id else category for c in self.categories
        ]
