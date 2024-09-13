from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)


from src.core.genre.domain.genre_repository import GenreFilter
from src.core.genre.application.use_cases.common.genre_output import GenreOutput
from src.core.genre.application.use_cases.create_genre import (
    CreateGenreInput,
    CreateGenreUseCase,
)
from src.core.genre.application.use_cases.delete_genre import (
    DeleteGenreInput,
    DeleteGenreUseCase,
)
from src.core.genre.application.use_cases.list_genres import (
    ListGenresInput,
    ListGenresUseCase,
)
from src.core.genre.application.use_cases.update_genre import (
    UpdateGenreInput,
    UpdateGenreUseCase,
)
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    DeleteGenreInputSerializer,
    UpdateGenreInputSerializer,
)
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.django_project.genre_app.repository import GenreDjangoRepository
from src.django_project.genre_app.presenters import (
    GenreCollectionPresenter,
    GenrePresenter,
)
from src.django_project.shared_app.filter_extractor import FilterExtractor


class GenreViewSet(viewsets.ViewSet, FilterExtractor):
    def __init__(self, **kwargs):
        genre_repo = GenreDjangoRepository()
        category_repo = CategoryDjangoRepository()

        self.create_use_case = CreateGenreUseCase(genre_repo, category_repo)
        self.list_use_case = ListGenresUseCase(genre_repo)
        self.update_use_case = UpdateGenreUseCase(genre_repo, category_repo)
        self.delete_use_case = DeleteGenreUseCase(genre_repo)

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenreInput(**serializer.validated_data)
        output = self.create_use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=GenreViewSet.serialize(output),
        )

    def list(self, request: Request) -> Response:
        query_params = request.query_params.dict()

        filters = self.extract_filters(query_params)
        input = ListGenresInput(
            **query_params,
            filter=(
                GenreFilter(
                    name=filters.get("name"),
                    categories_id=filters.get("categories_id"),
                )
            )
        )
        output = self.list_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=GenreCollectionPresenter(output=output).serialize(),
        )

    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateGenreInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateGenreInput(**serializer.validated_data)
        output = self.update_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=GenreViewSet.serialize(output),
        )

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteGenreInput(**serializer.validated_data)

        self.delete_use_case.execute(input=input)

        return Response(status=HTTP_204_NO_CONTENT)

    @staticmethod
    def serialize(output: GenreOutput):
        return GenrePresenter.from_output(output).serialize()
