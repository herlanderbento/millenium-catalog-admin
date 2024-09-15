from abc import ABC, abstractmethod
from pathlib import Path


class IStorage(ABC):
    @abstractmethod
    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        pass

    @abstractmethod
    def get(self, file_path: Path) -> bytes:
        pass
