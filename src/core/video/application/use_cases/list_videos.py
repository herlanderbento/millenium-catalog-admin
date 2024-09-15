from dataclasses import dataclass

from src.core._shared.application.pagination_output import PaginationOutput
from src.core._shared.application.search_input import SearchInput
from src.core._shared.application.use_cases import UseCase
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.video_repository import (
    IVideoRepository,
    VideoFilter,
    VideoSearchParams,
    VideoSearchResult,
)


@dataclass(slots=True)
class ListVideosInput(SearchInput[VideoFilter]):
    pass


@dataclass(slots=True)
class ListVideosOutput(PaginationOutput[VideoOutput]):
    pass


class ListVideosUseCase(UseCase):
    def __init__(self, video_repo: IVideoRepository):
        self.video_repo = video_repo

    def execute(self, input: ListVideosInput) -> ListVideosOutput:
        params = VideoSearchParams(**input.to_input())

        result = self.video_repo.search(params)

        return self.__to_output(result)

    def __to_output(self, result: VideoSearchResult) -> ListVideosOutput:
        items = list(map(VideoOutput.from_entity, result.items))
        return ListVideosOutput.from_search_result(items, result)
