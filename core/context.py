from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from instaloader.instaloader import Instaloader
from minio import Minio
from peewee import Model, PostgresqlDatabase
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from .options import AMQPOptions


class InstaminerState(Enum):
    IDLE = 0
    RUNNING = 1
    DRAINING = 2
    CLOSING = 3


@dataclass
class InstaminerContext:
    loader: Instaloader
    data_dir: str
    last_images: Dict[str, str]

    state: InstaminerState = InstaminerState.IDLE

    max_saved_memory_images: int = 10
    new_post_name: str = "new_post"
    new_post_update_name: str = "updated_post"
    queue_name: str = "instaminer"

    minio_client: Optional[Minio] = None
    amqp_connection: Optional[BlockingConnection] = None
    amqp_channel: Optional[BlockingChannel] = None
    db: Optional[PostgresqlDatabase] = None

    s3_endpoint: Optional[str] = None
    s3_bucket: Optional[str] = None

    PostModel: Optional[Model] = None

    amqp_options: Optional[AMQPOptions] = None