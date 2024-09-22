from abc import ABC, abstractmethod
from typing import List, Set
from src.core._shared.domain.repositories.repository_interface import ISearchableRepository
from src.core._shared.domain.repositories.search_params import SearchParams
from src.core._shared.domain.repositories.search_result import SearchResult
from src.core.category.domain.category import Category, CategoryId


class CategorySearchParams(SearchParams[str]):
    pass


class CategorySearchResult(SearchResult[Category]):
    pass


class ICategoryRepository(ISearchableRepository[Category, CategoryId], ABC):
    pass
