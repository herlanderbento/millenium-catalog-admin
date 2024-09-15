from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


from src.core.video.application.use_cases.delete_video import (
    DeleteVideoInput,
    DeleteVideoUseCase,
)
from src.core.video.domain.video_repository import VideoFilter
from src.core.video.application.use_cases.get_video import (
    GetVideoInput,
    GetVideoUseCase,
)
from src.core.video.application.use_cases.list_videos import (
    ListVideosInput,
    ListVideosUseCase,
)
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.application.use_cases.create_video import (
    CreateVideoInput,
    CreateVideoUseCase,
)

from src.django_project.shared_app.filter_extractor import FilterExtractor
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.django_project.genre_app.repository import GenreDjangoRepository
from src.django_project.video_app.presenters import (
    VideoCollectionPresenter,
    VideoPresenter,
)
from src.django_project.video_app.repository import VideoDjangoRepository
from src.django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    DeleteVideoInputSerializer,
    GetVideoInputSerializer,
)


class VideoViewSet(viewsets.ViewSet, FilterExtractor):
    def __init__(self, **kwargs):
        video_repo = VideoDjangoRepository()
        category_repo = CategoryDjangoRepository()
        genre_repo = GenreDjangoRepository()
        cast_member_repo = CastMemberDjangoRepository()

        self.create_use_case = CreateVideoUseCase(
            video_repo,
            category_repo,
            genre_repo,
            cast_member_repo,
        )
        self.get_use_case = GetVideoUseCase(video_repo)
        self.list_use_case = ListVideosUseCase(video_repo)
        self.delete_use_case = DeleteVideoUseCase(video_repo)

    def create(self, request: Request) -> Response:
        serializer = CreateVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVideoInput(**serializer.validated_data)
        output = self.create_use_case.execute(input)

        return Response(
            status=status.HTTP_201_CREATED,
            data=VideoViewSet.serialize(output),
        )

    def list(self, request: Request) -> Response:
        query_params = request.query_params.dict()

        filters = self.extract_filters(query_params)

        input = ListVideosInput(
            **query_params,
            filter=(
                VideoFilter(
                    title=filters.get("title"),
                    categories_id=filters.get("categories_id"),
                    genres_id=filters.get("genres_id"),
                    cast_members_id=filters.get("cast_members_id"),
                )
            )
        )
        output = self.list_use_case.execute(input)

        return Response(
            status=status.HTTP_200_OK,
            data=VideoCollectionPresenter(output).serialize(),
        )

    def retrieve(self, request: Request, pk: None) -> Response:
        serializer = GetVideoInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetVideoInput(**serializer.validated_data)
        output = self.get_use_case.execute(input)

        return Response(
            status=status.HTTP_200_OK,
            data=VideoViewSet.serialize(output),
        )

    def update(self, request: Request, pk: None):
        raise NotImplementedError

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteVideoInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteVideoInput(**serializer.validated_data)

        self.delete_use_case.execute(input)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def serialize(output: VideoOutput):
        return VideoPresenter.from_output(output).serialize()
