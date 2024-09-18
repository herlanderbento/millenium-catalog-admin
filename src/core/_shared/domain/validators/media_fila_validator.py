import hashlib
import random
import time


class MediaFileValidator:
    def __init__(self, max_size: int, valid_mime_types: list[str]):
        self.max_size = max_size
        self.valid_mime_types = valid_mime_types

    def validate(self, raw_name: str, size: int, mime_type: str):
        if not self.validate_size(size):
            raise InvalidMediaFileSizeError(size, self.max_size)

        if not self.validate_mime_type(mime_type):
            raise InvalidMediaFileMimeTypeError(mime_type, self.valid_mime_types)

        return {
            "name": self.generate_random_name(raw_name),
        }

    def validate_size(self, size: int) -> bool:
        return size <= self.max_size

    def validate_mime_type(self, mime_type: str) -> bool:
        return mime_type in self.valid_mime_types

    def generate_random_name(self, raw_name: str) -> str:
        extension = raw_name.split(".")[-1]  # Obtém a extensão do arquivo
        random_data = raw_name + str(random.random()) + str(time.time())
        hashed_name = hashlib.sha256(random_data.encode()).hexdigest()

        return f"{hashed_name}.{extension}"


class InvalidMediaFileSizeError(Exception):
    def __init__(self, actual_size: int, max_size: int):
        super().__init__(f"Invalid media file size: {actual_size} > {max_size}")


class InvalidMediaFileMimeTypeError(Exception):
    def __init__(self, actual_mime_type: str, valid_mime_types: list[str]):
        super().__init__(
            f"Invalid media file mime type: {actual_mime_type} not in {', '.join(valid_mime_types)}"
        )
