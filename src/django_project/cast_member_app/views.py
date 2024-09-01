from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

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
from src.core.cast_member.application.use_cases.common.exceptions import (
    CastMemberInvalidError,
    CastMemberNotFoundError,
)
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMemberInput,
    CreateCastMemberUseCase,
)
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberInputSerializer,
    CreateCastMemberOutputSerializer,
    DeleteCastMemberInputSerializer,
    GetCastMemberInputSerializer,
    GetCastMemberOutputSerializer,
    ListCastMembersOutputSerializer,
    UpdateCastMemberInputSerializer,
    UpdateCastMemberOutputSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCastMemberInput(**serializer.validated_data)
        use_case = CreateCastMemberUseCase(
            cast_member_repository=CastMemberDjangoRepository()
        )
        try:
            output = use_case.execute(input=input)
        except CastMemberInvalidError as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(e)})

        response_serializer = CreateCastMemberOutputSerializer(output)
        return Response(
            status=HTTP_201_CREATED,
            data=response_serializer.data,
        )

    def list(self, request: Request) -> Response:
        use_case = ListCastMembersUseCase(
            cast_member_repository=CastMemberDjangoRepository()
        )

        output = use_case.execute(input=ListCastMembersInput())

        return Response(
            status=HTTP_200_OK,
            data=ListCastMembersOutputSerializer(output).data,
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = GetCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetCastMemberInput(**serializer.validated_data)
        use_case = GetCastMemberUseCase(
            cast_member_repository=CastMemberDjangoRepository()
        )

        try:
            output = use_case.execute(input=input)
        except CastMemberNotFoundError as e:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(e)})

        return Response(
            status=HTTP_200_OK,
            data=GetCastMemberOutputSerializer(output).data,
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
        use_case = UpdateCastMemberUseCase(
            cast_member_repository=CastMemberDjangoRepository()
        )

        try:
            output = use_case.execute(input=input)
        except CastMemberNotFoundError as e:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(e)})
        except CastMemberInvalidError as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(e)})

        return Response(
            status=HTTP_200_OK,
            data=UpdateCastMemberOutputSerializer(output).data,
        )

    # def update(self, request: Request, pk: None) -> Response:

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteCastMemberInput(**serializer.validated_data)
        use_case = DeleteCastMemberUseCase(
            cast_member_repository=CastMemberDjangoRepository()
        )

        try:
            use_case.execute(input=input)
        except CastMemberNotFoundError as e:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(e)})

        return Response(status=HTTP_204_NO_CONTENT)
