from dataclasses import dataclass
from enum import StrEnum, unique


@unique
class Rating(StrEnum):
    ER = "ER"
    L = "L"
    AGE_10 = "age_10"
    AGE_12 = "age_12"
    AGE_14 = "age_14"
    AGE_16 = "age_16"
    AGE_18 = "age_18"


@unique
class MediaStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass(frozen=True)
class ImageMedia:
    name: str
    raw_location: str


@unique
class MediaType(StrEnum):
    VIDEO = "video"
    TRAILER = "trailer"
    BANNER = "banner"
    THUMBNAIL = "thumbnail"
    THUMBNAIL_HALF = "thumbnail_half"


@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    media_type: MediaType

    def complete(self, encoded_location: str):
        return AudioVideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=self.media_type,
        )

    def fail(self):
        return AudioVideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=self.encoded_location,
            status=MediaStatus.ERROR,
            media_type=self.media_type,
        )
