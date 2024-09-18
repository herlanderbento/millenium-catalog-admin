from dataclasses import dataclass
import datetime
from decimal import Decimal

from src.core._shared.domain.events.domain_event_interface import IDomainEvent
from src.core.cast_member.domain.cast_member import CastMemberId
from src.core.category.domain.category import CategoryId
from src.core.genre.domain.genre import GenreId
from src.core.video.domain.audio_video_media import AudioVideoMedia, ImageMedia, Rating


@dataclass
class VideoCreatedEventProps:
    id: str
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    categories_id: set[CategoryId]
    genres_id: set[GenreId]
    created_at: datetime.datetime
    cast_members_id: set[CastMemberId]
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    published: bool = False


class VideoCreatedEvent(IDomainEvent):
    aggregate_id: str
    occurred_on: datetime
    event_version: int

    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    categories_id: set[CategoryId]
    genres_id: set[GenreId]
    cast_members_id: set[CastMemberId]
    created_at: datetime.datetime
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    published: bool = False

    def __init__(self, props: VideoCreatedEventProps):
        self.aggregate_id = props.id
        self.occurred_on = datetime.datetime.now(datetime.UTC)
        self.event_version = 1

        self.title = props.title
        self.description = props.description
        self.launch_year = props.launch_year
        self.duration = props.duration
        self.rating = props.rating
        self.opened = props.opened
        self.categories_id = props.categories_id
        self.genres_id = props.genres_id
        self.cast_members_id = props.cast_members_id
        self.banner = props.banner
        self.thumbnail = props.thumbnail
        self.thumbnail_half = props.thumbnail_half
        self.trailer = props.trailer
        self.video = props.video
        self.published = props.published
        self.created_at = props.created_at
