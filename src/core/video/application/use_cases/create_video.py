from dataclasses import dataclass
from decimal import Decimal

from src.core.cast_member.application.validations.cast_members_ids_exists_in_database_validator import (
    CastMembersIdExistsInDatabaseValidator,
)
from src.core.category.application.validations.categories_ids_exists_in_database_validator import (
    CategoriesIdExistsInDatabaseValidator,
)
from src.core.genre.application.validations.genres_ids_exists_in_database_validator import (
    GenresIdExistsInDatabaseValidator,
)
from src.core.video.domain.video import Video
from src.core._shared.application.use_cases import UseCase
from src.core.cast_member.domain.cast_member import CastMemberId

from src.core.category.domain.category import CategoryId
from src.core.genre.domain.genre import GenreId
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.audio_video_media import Rating
from src.core.video.domain.video_repository import IVideoRepository


@dataclass()
class CreateVideoInput:
    title: str
    description: str
    launch_year: int
    duration: Decimal
    opened: bool
    rating: Rating
    categories_id: set[CategoryId]
    genres_id: set[GenreId]
    cast_members_id: set[CastMemberId]


@dataclass()
class CreateVideoOutput(VideoOutput):
    pass


class CreateVideoUseCase(UseCase):
    def __init__(
        self,
        video_repo: IVideoRepository,
        categories_id_validator: CategoriesIdExistsInDatabaseValidator,
        genres_id_validator: GenresIdExistsInDatabaseValidator,
        cast_members_id_validator: CastMembersIdExistsInDatabaseValidator,
    ):
        self.video_repo = video_repo
        self.categories_id_validator = categories_id_validator
        self.genres_id_validator = genres_id_validator
        self.cast_members_id_validator = cast_members_id_validator

    def execute(self, input: CreateVideoInput) -> CreateVideoOutput:
        self.categories_id_validator.validate(input.categories_id)
        self.genres_id_validator.validate(input.genres_id)
        self.cast_members_id_validator.validate(input.cast_members_id)

        video = Video.create(input)

        self.video_repo.insert(video)

        return self.__to_output(video)

    def __to_output(self, video: Video):
        return CreateVideoOutput.from_entity(video)
