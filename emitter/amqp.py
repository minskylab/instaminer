from typing import Tuple
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel


def open_amqp_connection() -> Tuple[BlockingConnection, BlockingChannel]:
    connection = BlockingConnection()
    channel = connection.channel()

    return connection, channel
