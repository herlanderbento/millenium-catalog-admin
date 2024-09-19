from django.dispatch import receiver

from src.core._shared.application.domain_event_handler_interface import IIntegrationEventHandler
from src.core._shared.application.message_broker_interface import IMessageBroker
from src.core.video.domain.domain_events.video_audio_media_replaced_event import VideoAudioMediaUploadedIntegrationEvent


class PublishVideoMediaReplacedInQueueHandler(IIntegrationEventHandler):

    def __init__(self, message_broker: IMessageBroker):
      print(f"message_broker {message_broker}")
        # self.message_broker = message_broker
        
    @receiver(VideoAudioMediaUploadedIntegrationEvent.__name__)
    def handle(self, event: VideoAudioMediaUploadedIntegrationEvent) -> None:
        # Publish event to video media replaced in queue queue
        pass  