from typing import List, Union
from uuid import UUID
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.domain.category import Category, CategoryId
from src.core.category.domain.category_repository import ICategoryRepository


class CategoriesIdExistsInDatabaseValidator:
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    def validate(
        self, categories_id: set[CategoryId]
    ) -> Union[List[UUID], List[NotFoundException]]:
        # categories_id_list = [str(id) for id in categories_id]

        # if not all(isinstance(v, str) for v in categories_id_list):
        #     raise ValueError("Invalid input: categories_id should be a list of strings")

        # try:
        #     categories_uuid = [UUID(v) for v in categories_id_list]
        # except ValueError as e:
        #     raise ValueError("One or more IDs are not valid UUIDs") from e

        exists_result = self.category_repo.exists_by_id(categories_id)

        if exists_result["not_exists"]:
            not_found_ids = [str(id) for id in exists_result["not_exists"]]
            raise NotFoundException(", ".join(not_found_ids), Category)

        return categories_id
