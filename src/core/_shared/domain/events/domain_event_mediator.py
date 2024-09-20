import logging
from typing import Type, List

from src.core._shared.domain.events.domain_event_interface import IDomainEvent, IIntegrationEvent, TDomainEvent
from src.core._shared.infra.message_broker.rabbitmq_message_broker import RabbitMQMessageBroker
from src.core._shared.application.handlers import Handler

from src.core.video.application.handlers.publish_video_media_replaced_in_queue_handler import (
    PublishVideoMediaReplacedInQueueHandler,
    DummyHandler,
)
from src.core.video.domain.domain_events.video_audio_media_uploaded_integration import (
    VideoAudioMediaUploadedIntegrationEvent,
)
from src.core.video.domain.domain_events.video_created_event import VideoCreatedEvent
logger = logging.getLogger(__name__)


# class DomainEventMediator(IIntegrationEvent):
#     def __init__(self):
#         self.handlers: dict[Type[TDomainEvent], List[Handler[TDomainEvent]]] = {
#             VideoAudioMediaUploadedIntegrationEvent: [
#                 PublishVideoMediaReplacedInQueueHandler(
#                     message_broker=RabbitMQMessageBroker(queue="videos.new")
#                 ),
#             ],
#             VideoCreatedEvent: [
#                 DummyHandler(),
#             ],
#         }

#     def handle(self, events: list[IDomainEvent]) -> None:
#         for event in events:
#             for handler in self.handlers[type(event)]:
#                 try:
#                     handler.handle(event)
#                 except Exception:
#                     logger.exception("Exception handling event %s", event)
#                     continue



class DomainEventMediator(IIntegrationEvent):
    def __init__(self):
        # Associa o evento de integração ao handler que deve processá-lo
        self.handlers: dict[Type[TDomainEvent], List[Handler[TDomainEvent]]] = {
            VideoAudioMediaUploadedIntegrationEvent: [
                PublishVideoMediaReplacedInQueueHandler(
                    message_broker=RabbitMQMessageBroker(queue="videos.new")
                ),
            ],
            VideoCreatedEvent: [
                DummyHandler(),  # Handler vazio ou qualquer outro necessário
            ],
        }

    def handle(self, events: list[IDomainEvent]) -> None:
        for event in events:
            event_type = type(event)

            if event_type == VideoCreatedEvent:
                integration_event = VideoAudioMediaUploadedIntegrationEvent(
                    resource_id=f"{event.aggregate_id}.{event.media_type}",
                    file_path=event.file_path
                )

                self._handle_integration_event(integration_event)
            else:
                self._handle_event(event)

    def _handle_event(self, event: IDomainEvent) -> None:
        event_type = type(event)
        for handler in self.handlers.get(event_type, []):
            try:
                handler.handle(event)
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def _handle_integration_event(self, integration_event: VideoAudioMediaUploadedIntegrationEvent) -> None:
        for handler in self.handlers.get(type(integration_event), []):
            try:
                handler.handle(integration_event)
            except Exception:
                logger.exception("Exception handling integration event %s", integration_event)
                continue
