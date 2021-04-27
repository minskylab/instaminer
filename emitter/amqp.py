# from typing import Tuple
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from dataclasses import dataclass


@dataclass
class AMQPOptions:
    host: str = "localhost"


def open_amqp_connection(opts: AMQPOptions) -> BlockingConnection:
    # Tuple[BlockingConnection, BlockingChannel]
    params = ConnectionParameters(host=opts.host)

    connection = BlockingConnection(params)
    # channel = connection.channel()

    return connection
