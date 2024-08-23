from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
)
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFound,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)

from django_project.category_app.repository import DjangoORMCategoryRepository


class CategoryViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(output).data,
        )

    def list(self, request: Request) -> Response:
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=ListCategoryRequest())

        response_serializer = ListCategoryResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetCategoryRequest(**serializer.validated_data)
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveCategoryResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk: UUID = None):
        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteCategoryRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteCategoryRequest(**request_data.validated_data)
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
