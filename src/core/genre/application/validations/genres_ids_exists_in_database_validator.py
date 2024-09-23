from typing import List, Union
from uuid import UUID
from src.core._shared.domain.exceptions import NotFoundException
from src.core.genre.domain.genre import Genre, GenreId
from src.core.genre.domain.genre_repository import IGenreRepository


class GenresIdExistsInDatabaseValidator:
    def __init__(self, genre_repo: IGenreRepository):
        self.genre_repo = genre_repo

    def validate(
        self, genres_id: set[GenreId]
    ) -> Union[List[UUID], List[NotFoundException]]:

        exists_result = self.genre_repo.exists_by_id(genres_id)

        if exists_result["not_exists"]:
            not_found_ids = [str(id) for id in exists_result["not_exists"]]
            raise NotFoundException(", ".join(not_found_ids), Genre)

        return genres_id
