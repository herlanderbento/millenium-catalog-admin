from pathlib import Path
from src.core._shared.application.storage_interface import IStorage


class LocalStorage(IStorage):
    TMP_BUCKET = "/tmp/millenium-storage"

    def __init__(self, bucket: str = TMP_BUCKET):
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        full_path = self.bucket.joinpath(file_path)

        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)

        with open(full_path, "wb") as file:
            file.write(content)

        return full_path.as_uri()

    def get(self, file_path: Path) -> bytes:
        with open(self.bucket.joinpath(file_path), "rb") as file:
            return file.read()
