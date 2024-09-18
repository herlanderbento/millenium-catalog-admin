from abc import ABC
from dataclasses import asdict
from enum import StrEnum, unique


@unique
class AudioVideoMediaStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AudioVideoMedia(ABC):
    name: str
    raw_location: str
    encoded_location: str = None
    status: AudioVideoMediaStatus

    def __init__(
        self,
        name: str,
        raw_location: str,
        status: AudioVideoMediaStatus,
        encoded_location: str = None,
    ):
        self.name = name
        self.raw_location = raw_location
        self.status = status
        self.encoded_location = encoded_location
        
    def raw_url(self):
      return f"{self.raw_location}{self.name}"
    
    def to_dict(self):
        entity_dict = asdict(self)
        return entity_dict