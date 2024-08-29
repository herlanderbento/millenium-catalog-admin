from abc import ABC, abstractmethod
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberRepository(ABC):

    @abstractmethod
    def insert(self, entity: CastMember):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: UUID) -> CastMember | None:
        raise NotImplementedError

    @abstractmethod
    def findAll(self) -> list[CastMember]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: CastMember):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
