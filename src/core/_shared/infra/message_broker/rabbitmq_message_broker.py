import json

import pika

from src.core._shared.application.message_broker import IMessageBrokerProducer
from src.core._shared.domain.events.domain_event_interface import IDomainEvent


class RabbitMQMessageBroker(IMessageBrokerProducer):
    def __init__(self, host="localhost", queue="videos.new"):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.credentials = pika.PlainCredentials("admin", "admin")

    def publish_event(self, event: IDomainEvent) -> None:
        if not self.connection:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    credentials=self.credentials,
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(
            exchange="", routing_key=self.queue, body=json.dumps(event.payload)
        )
        print(f"Sent: {event} to queue {self.queue}")

    def close(self):
        self.connection.close()
