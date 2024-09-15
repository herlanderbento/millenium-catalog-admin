from dataclasses import dataclass
from typing import List, Tuple

from src.core.cast_member.domain.cast_member import CastMemberId
from src.core.category.domain.category import CategoryId
from src.core.genre.domain.genre import GenreId
from src.core.video.domain.audio_video_media import (
    AudioVideoMedia,
    ImageMedia,
    MediaType,
)
from src.core.video.domain.video import Video, VideoId
from src.django_project.video_app.models import VideoModel


@dataclass
class VideoRelations:
    categories_ids: List[str]
    genres_ids: List[str]
    cast_members_ids: List[str]


class VideoModelMapper:
    @staticmethod
    def to_model(entity: Video) -> Tuple["VideoModel", VideoRelations]:
        return VideoModel(
            id=entity.id.value,
            title=entity.title,
            description=entity.description,
            launch_year=entity.launch_year,
            duration=entity.duration,
            rating=entity.rating,
            opened=entity.opened,
            published=entity.published,
            created_at=entity.created_at,
        ), VideoRelations(
            categories_ids=[str(category_id) for category_id in entity.categories_id],
            genres_ids=[str(genre_id) for genre_id in entity.genres_id],
            cast_members_ids=[
                str(cast_member_id) for cast_member_id in entity.cast_members_id
            ],
        )

    @staticmethod
    def to_entity(model: VideoModel) -> Video:
        video = Video(
            id=VideoId(model.id),
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            duration=model.duration,
            rating=model.rating,
            opened=model.opened,
            published=model.published,
            categories_id={
                CategoryId(category.id) for category in model.categories.all()
            },
            genres_id={GenreId(genre.id) for genre in model.genres.all()},
            cast_members_id={
                CastMemberId(cast_member.id) for cast_member in model.cast_members.all()
            },
            created_at=model.created_at,
        )

        if model.banner:
            video.banner = ImageMedia(
                name=model.banner.name,
                raw_location=model.banner.raw_location,
            )

        if model.thumbnail:
            video.thumbnail = ImageMedia(
                name=model.thumbnail.name,
                raw_location=model.thumbnail.raw_location,
            )

        if model.thumbnail_half:
            video.thumbnail_half = ImageMedia(
                name=model.thumbnail_half.name,
                raw_location=model.thumbnail_half.raw_location,
            )

        if model.trailer:
            video.trailer = AudioVideoMedia(
                name=model.trailer.name,
                raw_location=model.trailer.raw_location,
                encoded_location=model.trailer.encoded_location,
                status=model.trailer.status,
                media_type=MediaType.TRAILER,
            )

        if model.video:
            video.video = AudioVideoMedia(
                name=model.video.name,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=model.video.status,
                media_type=MediaType.VIDEO,
            )

        return video
