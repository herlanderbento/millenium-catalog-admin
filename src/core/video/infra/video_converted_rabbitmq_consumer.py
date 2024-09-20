import json
import logging
from uuid import UUID

import pika

from src.core._shared.application.message_broker import IMessageBrokerConsumer
from src.core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMediaInput,
    ProcessAudioVideoMediaUseCase,
)
from src.core.video.domain.audio_video_media import MediaStatus, MediaType


from src.django_project.video_app.repository import (
    VideoDjangoRepository,
)

logger = logging.getLogger(__name__)


class VideoConvertedRabbitMQConsumer(IMessageBrokerConsumer):
    def __init__(self, host="localhost", queue="videos.converted"):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.credentials = pika.PlainCredentials("admin", "admin")

    def on_message(self, message):
        print(f"Received message: {message}")
        try:
            # Body payload
            message = json.loads(message)

            # Tratamento de erro
            error_message = message["error"]
            if error_message:
                aggregate_id_raw, _ = message["message"]["resource_id"].split(".")
                logger.error(
                    f"Error processing video {aggregate_id_raw}: {error_message}"
                )
                return

            # Serialização do evento
            aggregate_id_raw, media_type_raw = message["video"]["resource_id"].split(
                "."
            )
            aggregate_id = UUID(aggregate_id_raw)
            media_type = MediaType(media_type_raw)
            encoded_location = message["video"]["encoded_video_folder"]
            status = MediaStatus(message["status"])

            # Execução do caso de uso
            process_audio_video_media_input = ProcessAudioVideoMediaInput(
                video_id=aggregate_id,
                encoded_location=encoded_location,
                media_type=media_type,
                status=status,
            )
            print("Calling use case with input", process_audio_video_media_input)
            use_case = ProcessAudioVideoMediaUseCase(video_repo=VideoDjangoRepository())
            use_case.execute(request=process_audio_video_media_input)
        except Exception:
            logger.error(f"Error processing payload {message}", exc_info=True)
            return

    def start(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=self.credentials,
            )
        )
        self.channel = self.connection.channel()

        # Cria a fila se não existir
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message_callback
        )
        print("Consumer started. Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def on_message_callback(self, ch, method, properties, body):
        self.on_message(body)

    def stop(self):
        self.connection.close()
