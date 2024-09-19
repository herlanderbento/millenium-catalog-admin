from dataclasses import dataclass
import datetime
from typing import Any, Literal

from src.core._shared.domain.events.domain_event_interface import (
    IDomainEvent,
    IIntegrationEvent,
)
from src.core.video.domain.audio_video_media import AudioVideoMedia


class VideoAudioMediaReplaced(IDomainEvent):
    aggregate_id: str
    occurred_on: datetime
    event_version: int

    media: AudioVideoMedia
    media_type: Literal["video", "trailer"]

    def __init__(
        self,
        aggregate_id: str,
        media: AudioVideoMedia,
        media_type: Literal["video", "trailer"],
    ):
        # print(f"aggregate_id: {aggregate_id}")
        # print(f"media: {media}")
        # print(f"media_type: {media_type}")

        self.aggregate_id = aggregate_id
        self.occurred_on = datetime.datetime.now(datetime.UTC)
        self.event_version = 1

        self.media = media
        self.media_type = media_type

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
        print(f"resource_id: {props.aggregate_id.value}.{props.media_type}")
        print(f"file_path: {props.media.title}_{props.media_type}.mp4")
        print(f"video_id: {props.aggregate_id.value}, media: {props.media}")
        
        self.resource_id = f"{props.aggregate_id.value}.{props.media_type}"
        self.file_path = f"{props.media.title}_{props.media_type}.mp4"
        self.event_version = props.event_version
        self.occurred_on = props.occurred_on
        self.payload = {"video_id": props.aggregate_id.value, "media": props.media}
        self.event_name = self.__class__.__name__
