from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreOutputSerializer,
    ListGenreOutputSerializer,
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
      
  

