from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import NotFoundException
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import IVideoRepository


@dataclass
class DeleteVideoInput:
    id: UUID


@dataclass
class DeleteVideoOutput(VideoOutput):
    pass


class DeleteVideoUseCase(UseCase):
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    def execute(self, input: DeleteVideoInput) -> None:
        if video := self.video_repo.find_by_id(input.id):
            self.video_repo.delete(video.id.value)
        else:
            raise NotFoundException(input.id, Video)
