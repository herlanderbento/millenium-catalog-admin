from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.events.domain_event_interface import IDomainEvent
from src.core.video.domain.audio_video_media import MediaType


@dataclass(frozen=True)
class VideoCreatedEvent(IDomainEvent):
    aggregate_id: UUID
    media_type: MediaType
    file_path: str