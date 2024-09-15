from dataclasses import dataclass, field
import datetime
from decimal import Decimal
from typing import Annotated, Set

from pydantic import Strict
from src.core.cast_member.domain.cast_member import CastMemberId
from src.core.category.domain.category import CategoryId
from src.core.genre.domain.genre import GenreId
from src.core.video.domain.audio_video_media import (
    AudioVideoMedia,
    ImageMedia,
    MediaStatus,
    Rating,
)
from src.core._shared.domain.entity import AggregateRoot
from src.core._shared.domain.value_objects import Uuid


@dataclass
class VideoCreateCommand:
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    categories_id: set[CategoryId]
    genres_id: set[GenreId]
    cast_members_id: set[CastMemberId]


class VideoId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class Video(AggregateRoot):
    id: VideoId = field(default_factory=VideoId)
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    categories_id: set[CategoryId]
    genres_id: set[GenreId]
    cast_members_id: set[CastMemberId]

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    published: bool = False

    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(props: VideoCreateCommand) -> None:
        video = Video(
            title=props.title,
            description=props.description,
            launch_year=props.launch_year,
            duration=props.duration,
            rating=props.rating,
            opened=props.opened,
            categories_id=props.categories_id,
            genres_id=props.genres_id,
            cast_members_id=props.cast_members_id,
            published=False,
        )
        return video

    @property
    def entity_id(self) -> Uuid:
        return self.id.value

    def change_title(self, title: str):
        self.title = title
        self.validate()

    def change_description(self, description: str):
        self.description = description
        self.validate()

    def change_launch_year(self, launch_year: int):
        self.launch_year = launch_year
        self.validate()

    def change_duration(self, duration: Decimal):
        self.duration = duration
        self.validate()

    def change_rating(self, rating: Rating):
        self.rating = rating
        self.validate()

    def mark_as_opened(self) -> None:
        self.opened = True
        self.validate()

    def mark_as_not_opened(self) -> None:
        self.opened = False
        self.validate()

    def replace_banner(self, banner: ImageMedia):
        self.banner = banner
        self.validate()

    def replace_thumbnail(self, thumbnail: ImageMedia):
        self.thumbnail = thumbnail
        self.validate()

    def replace_thumbnail_half(self, thumbnail_half: ImageMedia):
        self.thumbnail_half = thumbnail_half
        self.validate()

    def replace_trailer(self, trailer: AudioVideoMedia):
        self.trailer = trailer
        self.validate()

    def replace_video(self, video: AudioVideoMedia):
        self.video = video
        self.validate()

    def sync_categories_id(self, categories_id: Set[CategoryId]):
        self.categories_id = {CategoryId(id_) for id_ in categories_id}
        self.validate()

    def sync_genres_id(self, genres_id: Set[GenreId]):
        self.genres_id = {GenreId(id_) for id_ in genres_id}
        self.validate()

    def sync_cast_members_id(self, cast_members_id: Set[CastMemberId]):
        self.cast_members_id = {CastMemberId(id_) for id_ in cast_members_id}
        self.validate()

    def process(self, status: MediaStatus, encoded_location: str = "") -> None:
        if status == MediaStatus.COMPLETED:
            self.video = self.video.complete(encoded_location)
            self.published()
        else:
            self.video = self.video.fail()

        self.validate()

    def published(self):
        if (
            self.trailer
            and self.video
            and self.trailer.status == MediaStatus.COMPLETED
            and self.video.status == MediaStatus.COMPLETED
        ):
            self.published = True

    def validate(self):
        self._validate(
            {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "launch_year": self.launch_year,
                "duration": self.duration,
                "rating": self.rating,
                "opened": self.opened,
                "published": self.published,
                "categories_id": self.categories_id,
                "genres_id": self.genres_id,
                "cast_members_id": self.cast_members_id,
                "banner": self.banner,
                "thumbnail": self.thumbnail,
                "thumbnail_half": self.thumbnail_half,
                "trailer": self.trailer,
                "video": self.video,
                "created_at": self.created_at,
            }
        )
