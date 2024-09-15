from dataclasses import dataclass
from uuid import UUID

from src.core.video.domain.audio_video_media import MediaType
from src.core._shared.events.event import Event


@dataclass(frozen=True)
class AudioVideoMediaUpdated(Event):
    aggregate_id: UUID
    media_type: MediaType
    file_path: str
