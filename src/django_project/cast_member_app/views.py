from typing import Dict
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

from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)
from src.django_project.cast_member_app.presenters import (
    CastMemberCollectionPresenter,
    CastMemberPresenter,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberFilter

from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMemberInput,
    UpdateCastMemberUseCase,
)
from src.core.cast_member.application.use_cases.get_cast_member import (
    GetCastMemberInput,
    GetCastMemberUseCase,
)
from src.core.cast_member.application.use_cases.list_cast_members import (
    ListCastMembersInput,
    ListCastMembersUseCase,
)

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMemberInput,
    CreateCastMemberUseCase,
)
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberInputSerializer,
    DeleteCastMemberInputSerializer,
    GetCastMemberInputSerializer,
    UpdateCastMemberInputSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        cast_member_repository = CastMemberDjangoRepository()

        self.create_use_case = CreateCastMemberUseCase(cast_member_repository)
        self.list_use_case = ListCastMembersUseCase(cast_member_repository)
        self.get_use_case = GetCastMemberUseCase(cast_member_repository)
        self.update_use_case = UpdateCastMemberUseCase(cast_member_repository)
        self.delete_use_case = DeleteCastMemberUseCase(cast_member_repository)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCastMemberInput(**serializer.validated_data)

        output = self.create_use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=CastMemberViewSet.serialize(output),
        )

    def list(self, request: Request) -> Response:
        query_params = request.query_params.dict()

        filters = self.extract_filters(query_params)
        input = ListCastMembersInput(
            **query_params,
            filter=(
                CastMemberFilter(
                    name=filters.get("name"),
                    type=filters.get("type"),
                )
            )
        )

        output = self.list_use_case.execute(input)

        return Response(
            status=HTTP_200_OK,
            data=CastMemberCollectionPresenter(output=output).serialize(),
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = GetCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetCastMemberInput(**serializer.validated_data)

        output = self.get_use_case.execute(input=input)

        return Response(
            status=HTTP_200_OK,
            data=CastMemberViewSet.serialize(output),
        )

    def update(self, request: Request, pk: None) -> Response:
        serializer = UpdateCastMemberInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)
        input = UpdateCastMemberInput(**serializer.validated_data)

        output = self.update_use_case.execute(input=input)

        return Response(
            status=HTTP_200_OK,
            data=CastMemberViewSet.serialize(output),
        )

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteCastMemberInput(**serializer.validated_data)

        self.delete_use_case.execute(input=input)

        return Response(status=HTTP_204_NO_CONTENT)

    @staticmethod
    def serialize(output: CastMemberOutput):
        return CastMemberPresenter.from_output(output).serialize()

    @staticmethod
    def extract_filters(query_params: Dict[str, str]) -> Dict[str, str]:
        filters = {}
        keys_to_remove = []

        for key, value in query_params.items():
            if key.startswith("filter[") and key.endswith("]"):
                filter_key = key[len("filter[") : -1]
                filters[filter_key] = value
                keys_to_remove.append(key)

        for key in keys_to_remove:
            query_params.pop(key)

        return filters
