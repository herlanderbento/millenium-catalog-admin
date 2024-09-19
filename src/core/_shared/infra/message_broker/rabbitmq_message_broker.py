import json
import pika
from src.core._shared.application.message_broker_interface import IMessageBroker
from src.core._shared.domain.events.domain_event_interface import IIntegrationEvent


class RabbitMQMessageBroker(IMessageBroker):
    # def __init__(self,  host="localhost", queue_name="videos.new"):
    #     self.channel = self.connection.channel()
    #     self.channel.queue_declare(queue=queue_name)
    #     self.queue_name = queue_name
    #     self.credentials = pika.PlainCredentials("admin", "admin")
    #     self.connection = pika.BlockingConnection(
    #         pika.ConnectionParameters(host, credentials=self.credentials)
    #     )
    def __init__(self, host="localhost", queue="videos.new"):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.credentials = pika.PlainCredentials("admin", "admin")

    def publish(self, event: IIntegrationEvent) -> None:
        # self.channel.basic_publish(
        #     exchange="", routing_key=self.queue_name, body=json.dumps(event)
        # )
        if not self.connection:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, credentials=self.credentials)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(
            exchange="", routing_key=self.queue, body=json.dumps(event)
        )
        print(f"Sent: {event} to queue {self.queue}")

    def close(self):
        self.connection.close()
