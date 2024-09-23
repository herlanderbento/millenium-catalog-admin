import logging
from typing import List, Union
from uuid import UUID
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.domain.category import Category, CategoryId
from src.core.category.domain.category_repository import ICategoryRepository


class CategoriesIdExistsInDatabaseValidator:
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    # def validate(
    #     self, categories_id: List[str]
    # ) -> Union[List[UUID], List[NotFoundException]]:
    #     categories_uuid = [UUID(v) for v in categories_id]

    #     exists_result = self.category_repo.exists_by_id(categories_uuid)

    #     if exists_result["not_exists"]:
    #         return [
    #             NotFoundException(c.value, Category)
    #             for c in exists_result["not_exists"]
    #         ]

    #     return categories_uuid

    # def validate(self, categories_id: List[str]) -> Union[List[UUID], List[NotFoundException]]:
    #     # Convertendo cada ID para UUID, e garantindo que é uma string válida
    #     try:
    #         categories_uuid = [UUID(v) for v in categories_id]
    #     except ValueError as e:
    #         raise ValueError("One or more IDs are not valid UUIDs") from e

    #     # Verificando quais IDs existem no banco de dados
    #     exists_result = self.category_repo.exists_by_id(categories_uuid)

    #     # Se houver IDs não encontrados, retorna uma lista de NotFoundException
    #     if exists_result['not_exists']:
    #         return [NotFoundException(c, 'Category') for c in exists_result['not_exists']]

    #     # Se todos os IDs existirem, retorna a lista de UUIDs
    #     return categories_uuid

    def validate(
        self, categories_id: set[CategoryId]
    ) -> Union[List[UUID], List[NotFoundException]]:
        categories_id_list = [str(id) for id in categories_id]

        if not all(isinstance(v, str) for v in categories_id_list):
            raise ValueError("Invalid input: categories_id should be a list of strings")

        try:
            categories_uuid = [UUID(v) for v in categories_id_list]
        except ValueError as e:
            raise ValueError("One or more IDs are not valid UUIDs") from e

        exists_result = self.category_repo.exists_by_id(categories_uuid)

        if exists_result["not_exists"]:
            return [
                NotFoundException(c, Category) for c in exists_result["not_exists"]
            ]

        return categories_uuid
