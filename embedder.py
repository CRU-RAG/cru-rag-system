"""
Embedder
"""

import json
import os
import pika
from dotenv import load_dotenv
from services.weaviate.weaviate_service import WeaviateService

load_dotenv(override=True)
weaviate_service = WeaviateService()


def callback(ch, method, properties, body):
    """

    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    try:
        message = json.loads(body).get("data")
        weaviate_service.insert_data(
            message.get("id"), message.get("title"), message.get("body")
        )
        print("Message processed:", message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error processing message:", e)


def receive_message():
    """

    :return:
    """
    credentials = pika.PlainCredentials(
        os.environ.get("RABBIT_MQ_USERNAME"), os.environ.get("RABBIT_MQ_PASSWORD")
    )
    parameters = pika.ConnectionParameters(
        os.environ.get("RABBIT_MQ_HOST"),
        os.environ.get("RABBIT_MQ_PORT"),
        os.environ.get("RABBIT_MQ_VHOST"),
        credentials,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=5)
    channel.queue_declare(queue=os.environ.get("RABBIT_MQ_QUEUE"))
    channel.basic_consume(
        queue=os.environ.get("RABBIT_MQ_QUEUE"),
        on_message_callback=callback,
        auto_ack=False,
    )

    print(" [*] Waiting for contents. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    receive_message()
