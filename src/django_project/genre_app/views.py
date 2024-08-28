from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreOutputSerializer,
    DeleteGenreInputSerializer,
    ListGenreOutputSerializer,
    UpdateGenreInputSerializer,
)
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.django_project.genre_app.repository import GenreDjangoRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre


class GenreViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(
            genre_repository=GenreDjangoRepository(),
            category_repository=CategoryDjangoRepository(),
        )

        try:
            output = use_case.execute(input)
        except (InvalidGenre, RelatedCategoriesNotFound) as error:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(error)})

        return Response(
            status=HTTP_201_CREATED, data=CreateGenreOutputSerializer(output).data
        )

    def list(self, request: Request) -> Response:
        use_case = ListGenre(
            genre_repository=GenreDjangoRepository(),
        )
        output = use_case.execute(input=ListGenre.Input())

        return Response(status=HTTP_200_OK, data=ListGenreOutputSerializer(output).data)

    def update(self, request, pk: UUID = None):
        serializer = UpdateGenreInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer.validated_data)

        use_case = UpdateGenre(
            genre_repository=GenreDjangoRepository(),
            category_repository=CategoryDjangoRepository(),
        )

        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Genre with id {pk} not found"},
            )
        except (InvalidGenre, RelatedCategoriesNotFound) as error:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**serializer.validated_data)
        use_case = DeleteGenre(genre_repository=GenreDjangoRepository())

        try:
            use_case.execute(input)
        except GenreNotFound as error:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(error)})

        return Response(status=HTTP_204_NO_CONTENT)
