from dataclasses import dataclass

from src.core._shared.domain.events.domain_event_interface import IDomainEvent

@dataclass(frozen=True)
class VideoAudioMediaUploadedIntegrationEvent(IDomainEvent):
    resource_id: str
    file_path: str