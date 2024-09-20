from abc import ABC, abstractmethod

from src.core._shared.domain.events.domain_event_interface import IDomainEvent



class IMessageBrokerProducer(ABC):
    @abstractmethod
    def publish_event(self, event: IDomainEvent) -> None:
        pass

class IMessageBrokerConsumer(ABC):
    @abstractmethod
    def on_message(self, message: bytes):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass