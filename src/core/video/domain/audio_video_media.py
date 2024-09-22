from dataclasses import dataclass
from enum import StrEnum, unique
import hashlib
import random
import time

from src.core._shared.domain.validators.media_fila_validator import MediaFileValidator


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

    @staticmethod
    def create(name, raw_location, encoded_location, status, media_type):
        new_name = AudioVideoMedia.generate_random_name(
            raw_name=name
        )
        return AudioVideoMedia(
            name=new_name,
            raw_location=raw_location,
            encoded_location=encoded_location,
            status=status,
            media_type=media_type,
        )

    @staticmethod  # Torna o método estático
    def generate_random_name(raw_name: str) -> str:
        extension = raw_name.split(".")[-1]
        random_data = raw_name + str(random.random()) + str(time.time())
        hashed_name = hashlib.sha256(random_data.encode()).hexdigest()

        return f"{hashed_name}.{extension}"

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
