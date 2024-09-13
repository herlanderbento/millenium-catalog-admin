from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)


from src.core.category.application.use_cases.common.category_output import CategoryOutput
from src.core.category.application.use_cases.delete_category import (
    DeleteCategoryInput,
    DeleteCategoryUseCase,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategoryInput,
    UpdateCategoryUseCase,
)
from src.core.category.application.use_cases.create_category import (
    CreateCategoryInput,
    CreateCategoryUseCase,
)
from src.django_project.category_app.serializers import (
    CreateCategoryInputSerializer,
    DeleteCategoryInputSerializer,
    GetCategoryRequestSerializer,
    UpdateCategoryInputSerializer,
)
from src.core.category.application.use_cases.get_category import (
    GetCategoryInput,
    GetCategoryUseCase,
)
from src.core.category.application.use_cases.list_categories import (
    ListCategoriesInput,
    ListCategoriesUseCase,
)

from src.django_project.category_app.repository import CategoryDjangoRepository
from src.django_project.category_app.presenters import (
    CategoryCollectionPresenter,
    CategoryPresenter,
)


class CategoryViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        repository = CategoryDjangoRepository()

        self.create_use_case = CreateCategoryUseCase(repository)
        self.list_use_case = ListCategoriesUseCase(repository)
        self.get_use_case = GetCategoryUseCase(repository)
        self.update_use_case = UpdateCategoryUseCase(repository)
        self.delete_use_case = DeleteCategoryUseCase(repository)

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryInput(**serializer.validated_data)
        output = self.create_use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=CategoryViewSet.serialize(output),
        )

    def list(self, request: Request) -> Response:
        query_params = request.query_params.dict()

        input = ListCategoriesInput(**query_params)
        output = self.list_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=CategoryCollectionPresenter(output=output).serialize(),
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = GetCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetCategoryInput(**serializer.validated_data)
        output = self.get_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=CategoryViewSet.serialize(output),
        )

    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateCategoryInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryInput(**serializer.validated_data)
        output = self.update_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=CategoryViewSet.serialize(output),
        )

    def partial_update(self, request, pk: UUID = None):
        serializer = UpdateCategoryInputSerializer(
            data={
                **request.data,
                "id": pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryInput(**serializer.validated_data)
        output = self.update_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=CategoryViewSet.serialize(output),
        )

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteCategoryInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteCategoryInput(**serializer.validated_data)
        self.delete_use_case.execute(input)

        return Response(status=HTTP_204_NO_CONTENT)

    @staticmethod
    def serialize(output: CategoryOutput):
        return CategoryPresenter.from_output(output).serialize()
