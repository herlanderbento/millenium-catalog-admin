import unittest
from unittest.mock import create_autospec
import uuid

import pytest

from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre


class TestDeleteGenre(unittest.TestCase):

    def test_delete_genre(self):
        genre = Genre(
            id=uuid.uuid4(),
            name="Genre 1",
        )

        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(genre_repository=mock_repository)
        input = DeleteGenre.Input(
            id=genre.id,
        )

        use_case.execute(input)

        mock_repository.delete.assert_called_once_with(genre.id)

    def test_when_category_does_not_exist_then_raise_exception(self):
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteGenre(genre_repository=mock_repository)
        input = DeleteGenre.Input(
            id=uuid.uuid4(),
        )

        with pytest.raises(GenreNotFound, match=f"Genre with ID {input.id} not found"):
            use_case.execute(input)


if __name__ == "__main__":
    unittest.main()
