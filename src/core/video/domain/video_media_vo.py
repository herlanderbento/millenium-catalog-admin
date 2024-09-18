

from src.core._shared.domain.validators.media_fila_validator import MediaFileValidator
from src.core._shared.domain.audio_video_media_vo import AudioVideoMediaStatus
from src.core.video.domain.audio_video_media import AudioVideoMedia


class VideoMedia(AudioVideoMedia):
    max_size = 1024 * 1024 * 1024 * 50  # 50GB
    mime_types = ['video/mp4']

    @classmethod
    def create_from_file(cls, raw_name: str, mime_type: str, size: int, video_id: str):
        media_file_validator = MediaFileValidator(cls.max_size, cls.mime_types)
        
        validated = media_file_validator.validate({
            raw_name: raw_name,
            mime_type: mime_type,
            size: size
        })

        new_name = validated['name']
        return cls.create({
            'name': f"{video_id.id}-{new_name}",
            'raw_location': f"videos/{video_id.id}/videos"
        })

    @classmethod
    def create(cls, props: dict):
        return cls(
            name=props['name'],
            raw_location=props['raw_location'],
            status=AudioVideoMediaStatus.PENDING
        )

    def process(self):
        return VideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=self.encoded_location,
            status=AudioVideoMediaStatus.PROCESSING
        )

    def complete(self, encoded_location: str):
        return VideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=encoded_location,
            status=AudioVideoMediaStatus.COMPLETED
        )

    def fail(self):
        return VideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=self.encoded_location,
            status=AudioVideoMediaStatus.FAILED
        )