from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import NotFoundException
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import IVideoRepository


@dataclass
class GetVideoInput:
    id: UUID


@dataclass
class GetVideoOutput(VideoOutput):
    pass


class GetVideoUseCase(UseCase):
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    def execute(self, input: GetVideoInput) -> GetVideoOutput:
        if video := self.video_repo.find_by_id(input.id):
            return self.__to_output(video)
        else:
            raise NotFoundException(input.id, Video)

    def __to_output(self, video: Video) -> GetVideoOutput:
        return GetVideoOutput.from_entity(video)
