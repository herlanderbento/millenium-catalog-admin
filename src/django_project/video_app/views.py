from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from src.core._shared.application.application_service import ApplicationService
from src.core.cast_member.application.validations.cast_members_ids_exists_in_database_validator import (
    CastMembersIdExistsInDatabaseValidator,
)
from src.core.category.application.validations.categories_ids_exists_in_database_validator import (
    CategoriesIdExistsInDatabaseValidator,
)
from src.core.genre.application.validations.genres_ids_exists_in_database_validator import (
    GenresIdExistsInDatabaseValidator,
)
from src.core.video.application.use_cases.update_video import (
    UpdateVideoInput,
    UpdateVideoUseCase,
)
from src.core.video.application.use_cases.upload_image_media import (
    UploadImageMediaInput,
    UploadImageMediaUseCase,
)
from src.core._shared.domain.events.domain_event_mediator import DomainEventMediator
from src.core._shared.infra.storage.local_storage import LocalStorage
from src.core._shared.infra.storage.s3_storage import S3Storage
from src.core.video.application.use_cases.upload_audio_video_media import (
    UploadAudioVideoMediaInput,
    UploadAudioVideoMediaUseCase,
)
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
from src.django_project.shared_app.unit_of_work import UnitOfWork
from src.django_project.video_app.presenters import (
    VideoCollectionPresenter,
    VideoPresenter,
)
from src.django_project.video_app.repository import VideoDjangoRepository
from src.django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    DeleteVideoInputSerializer,
    GetVideoInputSerializer,
    UpdateVideoInputSerializer,
    UploadAudioVideoMediaInputSerializer,
    UploadImageMediaInputSerializer,
)


class VideoViewSet(viewsets.ViewSet, FilterExtractor):
    def __init__(self, **kwargs):
        video_repo = VideoDjangoRepository()
        category_repo = CategoryDjangoRepository()
        genre_repo = GenreDjangoRepository()
        cast_member_repo = CastMemberDjangoRepository()

        storage = S3Storage()
        local_storage = LocalStorage()

        uow = UnitOfWork()

        app_service = ApplicationService(
            uow=uow,
            domain_event_mediator=DomainEventMediator(),
        )

        categories_id_validator = CategoriesIdExistsInDatabaseValidator(category_repo)
        genres_id_validator = GenresIdExistsInDatabaseValidator(genre_repo)
        cast_members_id_validator = CastMembersIdExistsInDatabaseValidator(
            cast_member_repo
        )

        self.create_use_case = CreateVideoUseCase(
            video_repo,
            categories_id_validator,
            genres_id_validator,
            cast_members_id_validator,
        )
        self.get_use_case = GetVideoUseCase(video_repo)
        self.list_use_case = ListVideosUseCase(video_repo)
        self.delete_use_case = DeleteVideoUseCase(video_repo)
        self.update_use_case = UpdateVideoUseCase(
            video_repo,
            categories_id_validator,
            genres_id_validator,
            cast_members_id_validator,
        )
        self.upload_audio_video_media = UploadAudioVideoMediaUseCase(
            video_repo=video_repo,
            storage=storage,
            app_service=app_service,
        )
        self.upload_image_media = UploadImageMediaUseCase(video_repo, storage)

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
            ),
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

    def partial_update(self, request: Request, pk: None):
        serializer = UpdateVideoInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateVideoInput(**serializer.validated_data)
        output = self.update_use_case.execute(input)

        return Response(
            status=status.HTTP_200_OK,
            data=VideoViewSet.serialize(output),
        )

    @action(detail=True, methods=["patch"], url_path="upload-video")
    def upload_video(self, request: Request, pk: UUID = None):
        serializer = UploadAudioVideoMediaInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        field = request.FILES.get("video") or request.FILES.get("trailer")

        if not field:
            return Response(
                {"detail": "No video or trailer file uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = field

        input = UploadAudioVideoMediaInput(
            **serializer.validated_data,
            field="video" if "video" in request.FILES else "trailer",
            file_name=file.name,
            content=file.read(),
            content_type=file.content_type,
        )

        output = self.upload_audio_video_media.execute(input)

        return Response(
            status=status.HTTP_200_OK,
            data=VideoViewSet.serialize(output),
        )

    @action(detail=True, methods=["patch"], url_path="upload-images")
    def upload_image(self, request: Request, pk: UUID = None):
        serializer = UploadImageMediaInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        file_fields = {
            "banner": "banner",
            "thumbnail": "thumbnail",
            "thumbnail_half": "thumbnail_half",
        }

        field = next(
            (field for field, key in file_fields.items() if key in request.FILES),
            None,
        )

        if field is None:
            return Response(
                {"detail": "No banner, thumbnail, or thumbnail_half file uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = request.FILES[field]

        input = UploadImageMediaInput(
            **serializer.validated_data,
            field=field,
            file_name=file.name,
            content=file.read(),
            content_type=file.content_type,
        )

        output = self.upload_image_media.execute(input)

        return Response(
            status=status.HTTP_200_OK,
            data=VideoViewSet.serialize(output),
        )

    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteVideoInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteVideoInput(**serializer.validated_data)

        self.delete_use_case.execute(input)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def serialize(output: VideoOutput):
        return VideoPresenter.from_output(output).serialize()
