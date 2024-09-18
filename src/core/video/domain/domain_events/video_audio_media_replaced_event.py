from dataclasses import dataclass
import datetime
from typing import Any, Literal, Union

from src.core.video.domain.trailer_media_vo import TrailerMedia 
from src.core.video.domain.video_media_vo import VideoMedia 
from src.core._shared.domain.events.domain_event_interface import (
    IDomainEvent,
    IIntegrationEvent,
)
from src.core.video.domain.audio_video_media import AudioVideoMedia


@dataclass
class VideoAudioMediaReplacedProps:
    aggregate_id: str
    media: Union[TrailerMedia, VideoMedia]
    media_type: Literal["video", "trailer"]


class VideoAudioMediaReplaced(IDomainEvent):
    aggregate_id: str
    occurred_on: datetime
    event_version: int

    media: Union[TrailerMedia, VideoMedia]
    media_type: Literal["video", "trailer"]

    def __init__(self, props: VideoAudioMediaReplacedProps):
        self.aggregate_id = props.aggregate_id
        self.occurred_on = datetime.datetime.now(datetime.UTC)
        self.event_version = 1

        self.media = props.media
        self.media_type = props.media_type

    def get_integration_event(self) -> "VideoAudioMediaUploadedIntegrationEvent":
        return VideoAudioMediaUploadedIntegrationEvent(self)


class VideoAudioMediaUploadedIntegrationEvent(IIntegrationEvent):
    resource_id: str
    file_path: str

    event_name: str
    payload: Any
    event_version: int
    occurred_on: datetime = datetime.datetime.now(datetime.UTC)

    def __init__(self, props: VideoAudioMediaReplaced):
        self.resource_id = f"{props.aggregate_id.value}.{props.media_type}"
        self.file_path = f"{props.media.title}_{props.media_type}.mp4"
        self.event_version = props.event_version
        self.occurred_on = props.occurred_on
        self.payload = {"video_id": props.aggregate_id.value, "media": props.media}
        self.event_name = self.__class__.__name__
