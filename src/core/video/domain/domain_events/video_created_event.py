from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.events.domain_event_interface import IDomainEvent
from src.core.video.domain.audio_video_media import MediaType
from src.core.video.domain.domain_events.video_audio_media_uploaded_integration import VideoAudioMediaUploadedIntegrationEvent


@dataclass(frozen=True)
class VideoCreatedEvent(IDomainEvent):
    aggregate_id: UUID
    media_type: MediaType
    file_path: str
    
    def to_integration_event(self) -> VideoAudioMediaUploadedIntegrationEvent:
        return VideoAudioMediaUploadedIntegrationEvent(
            resource_id=f"{self.aggregate_id}.{self.media_type}",
            file_path=self.file_path
        )
