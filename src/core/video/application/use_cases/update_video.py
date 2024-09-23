from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.cast_member.application.validations.cast_members_ids_exists_in_database_validator import (
    CastMembersIdExistsInDatabaseValidator,
)
from src.core.cast_member.domain.cast_member import CastMemberId
from src.core.category.application.validations.categories_ids_exists_in_database_validator import (
    CategoriesIdExistsInDatabaseValidator,
)
from src.core.category.domain.category import CategoryId
from src.core.genre.application.validations.genres_ids_exists_in_database_validator import (
    GenresIdExistsInDatabaseValidator,
)
from src.core.genre.domain.genre import GenreId
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.audio_video_media import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import IVideoRepository


@dataclass
class UpdateVideoInput:
    id: UUID
    title: str
    description: str
    launch_year: int
    duration: Decimal
    opened: bool
    rating: Rating
    categories_id: set[CategoryId]
    genres_id: set[GenreId]
    cast_members_id: set[CastMemberId]


@dataclass
class UpdateVideoOutput(VideoOutput):
    pass


class UpdateVideoUseCase(UseCase):
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

    def execute(self, input: UpdateVideoInput) -> UpdateVideoOutput:
        video = self.video_repo.find_by_id(input.id)

        if video is None:
            raise NotFoundException(input.id, Video)

        self.categories_id_validator.validate(input.categories_id)
        self.genres_id_validator.validate(input.genres_id)
        self.cast_members_id_validator.validate(input.cast_members_id)

        if input.title is not None:
            video.change_title(input.title)

        if input.description is not None:
            video.change_description(input.description)

        if input.launch_year is not None:
            video.change_launch_year(input.launch_year)

        if input.duration is not None:
            video.change_duration(input.duration)

        if input.rating is not None:
            video.change_rating(input.rating)

        if input.categories_id is not None:
            video.sync_categories_id(input.categories_id)

        if input.genres_id is not None:
            video.sync_genres_id(input.genres_id)

        if input.cast_members_id is not None:
            video.sync_cast_members_id(input.cast_members_id)
            
        if input.opened is True:
           video.mark_as_opened()
        
        if input.opened is False:
            video.mark_as_not_opened()

        if video.notification.has_errors():
            raise EntityValidationException(video.notification.errors)

        self.video_repo.update(video)

        return self.__to_output(video)

    def __to_output(self, video: Video):
        return UpdateVideoOutput.from_entity(video)
