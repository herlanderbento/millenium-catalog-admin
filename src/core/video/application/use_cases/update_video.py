from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
    RelatedNotFoundException,
)
from src.core.video.domain.video import Video, VideoId
from src.core.cast_member.domain.cast_member_repository import ICastMemberRepository
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.genre.domain.genre_repository import IGenreRepository
from src.core.video.domain.video_repository import IVideoRepository
from src.core._shared.application.use_cases import UseCase
from src.core.cast_member.domain.cast_member import CastMemberId
from src.core.category.domain.category import CategoryId
from src.core.genre.domain.genre import GenreId
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.audio_video_media import Rating


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
        category_repo: ICategoryRepository,
        genre_repo: IGenreRepository,
        cast_member_repo: ICastMemberRepository,
    ):
        self.video_repo = video_repo
        self.category_repo = category_repo
        self.genre_repo = genre_repo
        self.cast_member_repo = cast_member_repo

    def execute(self, input: UpdateVideoInput) -> UpdateVideoOutput:
        video = self.video_repo.find_by_id(input.id)

        if video is None:
            raise NotFoundException(input.id, Video)

        self.__validate_categories(input.categories_id)
        self.__validate_genres(input.genres_id)
        self.__validate_cast_members(input.cast_members_id)

        if input.title is not None:
            video.change_title(input.title)

        if input.description is not None:
            video.change_description(input.description)

        if input.launch_year is not None:
            video.change_launch_year(input.launch_year)

        if input.duration is not None:
            video.change_duration(input.duration)

        if input.opened is not None:
            video.change_opened(input.opened)

        if input.rating is not None:
            video.change_rating(input.rating)

        if input.categories_id is not None:
            video.sync_categories_id(input.categories_id)

        if input.genres_id is not None:
            video.sync_genres_id(input.genres_id)

        if input.cast_members_id is not None:
            video.sync_cast_members_id(input.cast_members_id)

        if video.notification.has_errors():
            raise EntityValidationException(video.notification.errors)
        
        self.video_repo.update(video)

        return self.__to_output(video)

    def __validate_categories(self, categories_id: set[CategoryId]):
        categories_ids = {
            category.id for category in self.category_repo.find_by_ids(categories_id)
        }
        if len(categories_ids) != len(categories_id):
            raise RelatedNotFoundException(
                f"Categories with provided IDs not found: {categories_id - categories_ids}"
            )

    def __validate_genres(self, genres_id: set[GenreId]):
        genres_ids = {genre.id for genre in self.genre_repo.find_by_ids(genres_id)}
        if len(genres_ids) != len(genres_id):
            raise RelatedNotFoundException(
                f"Genres with provided IDs not found: {genres_id - genres_ids}"
            )

    def __validate_cast_members(self, cast_members_id: set[CastMemberId]):
        cast_member_ids = {
            cast_member.id
            for cast_member in self.cast_member_repo.find_by_ids(cast_members_id)
        }
        if len(cast_member_ids) != len(cast_members_id):
            raise RelatedNotFoundException(
                f"Cast Members with provided IDs not found: {cast_members_id - cast_member_ids}"
            )

    def __to_output(self, video: Video):
        return UpdateVideoOutput.from_entity(video)
