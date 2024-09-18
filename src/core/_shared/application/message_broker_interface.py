

from abc import ABC, abstractmethod

from src.core._shared.domain.events.domain_event_interface import IIntegrationEvent


class IMessageBroker(ABC):
  
    @abstractmethod
    def publish(self, event: IIntegrationEvent) -> None:
        pass
