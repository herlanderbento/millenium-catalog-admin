from dataclasses import dataclass
from typing import Literal
from uuid import UUID
from pathlib import Path

from src.core.video.application.events.integration_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.application.storage_interface import IStorage
from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.audio_video_media import (
    AudioVideoMedia,
    MediaStatus,
    MediaType,
)
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import IVideoRepository


@dataclass
class UploadAudioVideoMediaInput:
    id: UUID
    field: Literal["video", "trailer"]
    file_name: str
    content: bytes
    content_type: str


@dataclass
class UploadAudioVideoMediaOutput(VideoOutput):
    pass


class UploadAudioVideoMediaUseCase(UseCase):
    def __init__(
        self,
        video_repo: IVideoRepository,
        storage: IStorage,
        message_bus: MessageBus,
    ):
        self.video_repo = video_repo
        self.storage = storage
        self.message_bus = message_bus

    def execute(self, input: UploadAudioVideoMediaInput) -> UploadAudioVideoMediaOutput:
        video = self.video_repo.find_by_id(input.id)

        if video is None:
            raise NotFoundException(input.id, Video)

        file_path = Path("videos") / str(input.id) / input.file_name

        media_type_mapping = {
            "video": (MediaType.VIDEO, video.replace_video),
            "trailer": (MediaType.TRAILER, video.replace_trailer),
        }

        media_type, replace_function = media_type_mapping.get(input.field, (None, None))

        if media_type is None:
            raise EntityValidationException(f"Invalid field value: {input.field}")

        media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=media_type,
        )

        replace_function(media)

        self.storage.store(
            file_path,
            input.content,
            input.content_type,
        )

        self.video_repo.update(video)

        self.message_bus.handle(
            [
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=f"{input.id}.{MediaType.VIDEO}",
                    file_path=str(file_path),
                ),
            ]
        )

        return self.__to_output(video)

    def __to_output(self, video: Video) -> UploadAudioVideoMediaOutput:
        return UploadAudioVideoMediaOutput.from_entity(video)