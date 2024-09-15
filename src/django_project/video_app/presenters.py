from dataclasses import dataclass
import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import PlainSerializer

from src.core.video.application.use_cases.list_videos import ListVideosOutput
from src.core.video.application.use_cases.common.video_output import VideoOutput
from src.core.video.domain.audio_video_media import AudioVideoMedia, ImageMedia, Rating
from src.django_project.shared_app.presenters import (
    CollectionPresenter,
    ResourcePresenter,
)


@dataclass(slots=True)
class VideoPresenter(ResourcePresenter):
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
    created_at: Annotated[datetime.datetime, PlainSerializer(lambda x: x.isoformat())]

    @classmethod
    def from_output(cls, output: VideoOutput):
        return cls(
            id=output.id,
            title=output.title,
            description=output.description,
            launch_year=output.launch_year,
            duration=output.duration,
            rating=(
                Rating(output.rating)
                if isinstance(output.rating, str)
                else output.rating
            ),
            opened=output.opened,
            published=output.published,
            categories_id=output.categories_id,
            genres_id=output.genres_id,
            cast_members_id=output.cast_members_id,
            banner=output.banner,
            thumbnail=output.thumbnail,
            thumbnail_half=output.thumbnail_half,
            trailer=output.trailer,
            video=output.video,
            created_at=output.created_at,
        )


@dataclass(slots=True)
class VideoCollectionPresenter(CollectionPresenter):
    output: ListVideosOutput

    # def __post_init__(self):
    #     self.data = [
    #         VideoPresenter.from_output(
    #             id=item.id,
    #             title=item.title,
    #             description=item.description,
    #             launch_year=item.launch_year,
    #             duration=item.duration,
    #             rating=(
    #                 Rating(item.rating) if isinstance(item.rating, str) else item.rating
    #             ),
    #             opened=item.opened,
    #             published=item.published,
    #             categories_id=item.categories_id,
    #             genres_id=item.genres_id,
    #             cast_members_id=item.cast_members_id,
    #             banner=item.banner,
    #             thumbnail=item.thumbnail,
    #             thumbnail_half=item.thumbnail_half,
    #             trailer=item.trailer,
    #             video=item.video,
    #             created_at=item.created_at,
    #         )
    #         for item in self.output.items
    #     ]

    #     self.pagination = self.output

    def __post_init__(self):
        self.data = [
            VideoPresenter.from_output(item)  # Passar o objeto item diretamente
            for item in self.output.items
        ]

        self.pagination = self.output
