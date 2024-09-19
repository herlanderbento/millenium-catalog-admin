from abc import ABC, abstractmethod
from typing import Generic

from src.core._shared.domain.events.domain_event_interface import TDomainEvent



class Handler(ABC, Generic[TDomainEvent]):
    @abstractmethod
    def handle(self, event: TDomainEvent) -> None:
        pass