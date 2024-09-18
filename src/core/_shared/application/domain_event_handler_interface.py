from abc import ABC, abstractmethod
from src.core._shared.domain.events.domain_event_interface import IDomainEvent, IIntegrationEvent


class IDomainEventHandler(ABC):
    @abstractmethod
    def handle(self, event: IDomainEvent) -> None:
        pass

class IIntegrationEventHandler(ABC):
    @abstractmethod
    def handle(self, event: IIntegrationEvent) -> None:
        pass
