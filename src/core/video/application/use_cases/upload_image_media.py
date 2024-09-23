from dataclasses import dataclass
from typing import Literal
from uuid import UUID
from pathlib import Path

from src.core.video.domain.audio_video_media import ImageMedia
from src.core._shared.application.storage_interface import IStorage
from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import IVideoRepository
from src.core._shared.application.use_cases import UseCase
from src.core.video.application.use_cases.common.video_output import VideoOutput


@dataclass
class UploadImageMediaInput:
    id: UUID
    field: Literal["banner", "thumbnail", "thumbnail_half"]
    file_name: str
    content: bytes
    content_type: str


@dataclass
class UploadImageMediaOutput(VideoOutput):
    pass


class UploadImageMediaUseCase(UseCase):
    def __init__(
        self,
        video_repo: IVideoRepository,
        storage: IStorage,
    ):
        self.video_repo = video_repo
        self.storage = storage

    def execute(self, input: UploadImageMediaInput) -> UploadImageMediaOutput:
        video = self.video_repo.find_by_id(input.id)

        if video is None:
            raise NotFoundException(input.id, Video)

        field_mapping = {
            "banner": video.replace_banner,
            "thumbnail": video.replace_thumbnail,
            "thumbnail_half": video.replace_thumbnail_half,
        }

        replace_method = field_mapping.get(input.field)

        if replace_method is None:
            raise EntityValidationException(f"Invalid field value: {input.field}")

        file_path = Path("images") / str(input.id) / input.file_name

        image_media = ImageMedia(
            name=input.file_name,
            raw_location=str(file_path),
        )
        replace_method(image_media)

        self.storage.store(
            file_path,
            input.content,
            input.content_type,         
        )

        self.video_repo.update(video)

        return self.__to_output(video)

    def __to_output(self, video: Video) -> UploadImageMediaOutput:
        return UploadImageMediaOutput.from_entity(video)
