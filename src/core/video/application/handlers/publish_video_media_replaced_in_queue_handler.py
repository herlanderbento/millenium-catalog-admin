from src.core.video.domain.domain_events.video_created_event import VideoCreatedEvent
from src.core._shared.application.handlers import Handler
from src.core._shared.application.message_broker import IMessageBrokerProducer
from src.core.video.domain.domain_events.video_audio_media_uploaded_integration import (
    VideoAudioMediaUploadedIntegrationEvent,
)


class PublishVideoMediaReplacedInQueueHandler(
    Handler[VideoAudioMediaUploadedIntegrationEvent]
):
    def __init__(self, message_broker: IMessageBrokerProducer):
        print("calling rabbitmq init")
        self.message_broker = message_broker

    def handle(self, event: VideoAudioMediaUploadedIntegrationEvent) -> None:
        print(f"Dispatching integration event {event}")
        self.message_broker.publish_event(event)


class DummyHandler(Handler[VideoCreatedEvent]):
    def handle(self, event: VideoCreatedEvent) -> None:
        print(f"Handling domain event {event} with DummyHandler")
