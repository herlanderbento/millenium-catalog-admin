from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import NotFoundException
from src.core.video.domain.audio_video_media import MediaStatus, MediaType
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import IVideoRepository


@dataclass
class ProcessAudioVideoMediaInput:
    video_id: UUID
    encoded_location: str
    media_type: MediaType
    status: MediaStatus


class ProcessAudioVideoMediaUseCase(UseCase):
    def __init__(self, video_repo: IVideoRepository) -> None:
        self.video_repo = video_repo

    def execute(self, input: ProcessAudioVideoMediaInput) -> None:
        video = self.video_repo.find_by_id(input.video_id)

        if video is None:
            raise NotFoundException(input.video_id, Video)

        if input.media_type == MediaType.VIDEO:
            if not video.video:
                raise ValueError("Video must have a video media to be processed")

            video.process(input.status, input.encoded_location)

        self.video_repo.update(video)
