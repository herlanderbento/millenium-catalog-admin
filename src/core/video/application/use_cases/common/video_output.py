from dataclasses import dataclass
import datetime
from decimal import Decimal
from uuid import UUID

from src.core.video.domain.audio_video_media import AudioVideoMedia, ImageMedia, Rating
from src.core.video.domain.video import Video


@dataclass(slots=True)
class VideoOutput:
    id: UUID
    title: str
    description: str
    launch_year: int
    duration: Decimal
    rating: Rating
    opened: bool
    published: bool
    categories_id: set[str | UUID]
    genres_id: set[str | UUID]
    cast_members_id: set[str | UUID]
    banner: ImageMedia
    thumbnail: ImageMedia
    thumbnail_half: ImageMedia
    trailer: AudioVideoMedia
    video: AudioVideoMedia
    created_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: Video):
        return cls(
            id=entity.id.value,
            title=entity.title,
            description=entity.description,
            launch_year=entity.launch_year,
            duration=entity.duration,
            rating=entity.rating,
            opened=entity.opened,
            published=entity.published,
            categories_id={str(category_id) for category_id in entity.categories_id},
            genres_id={str(genres_id) for genres_id in entity.genres_id},
            cast_members_id={
                str(cast_members_id) for cast_members_id in entity.cast_members_id
            },
            banner=entity.banner,
            thumbnail=entity.thumbnail,
            thumbnail_half=entity.thumbnail_half,
            trailer=entity.trailer,
            video=entity.video,
            created_at=entity.created_at,
        )
