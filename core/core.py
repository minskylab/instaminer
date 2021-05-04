
from pika.adapters.blocking_connection import BlockingChannel
from pika import BlockingConnection
from dataclasses import dataclass
from typing import Dict, Optional
from minio import Minio
from instaloader.instaloader import Instaloader
from pathlib import Path
from peewee import Model, PostgresqlDatabase
from database import open_postgres_from_env
from enum import Enum
from collections import defaultdict
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from dataclasses import dataclass


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

    minio_client: Optional[Minio] = None
    amqp_client: Optional[BlockingConnection] = None
    amqp_channel: Optional[BlockingChannel] = None
    db: Optional[PostgresqlDatabase] = None

    s3_endpoint: Optional[str] = None
    s3_bucket: Optional[str] = None

    PostModel: Optional[Model] = None


@dataclass
class MinioOptions:
    endpoint: str
    access_key: str
    secret_key: str
    bucket: str
    ssl: bool
    region: str


def open_minio(opts: MinioOptions) -> Minio:
    endpoint = opts.endpoint
    access_key = opts.access_key
    secret_key = opts.secret_key
    bucket = opts.bucket
    ssl = opts.ssl
    region = opts.region

    m_client = Minio(endpoint,
                     access_key=access_key,
                     secret_key=secret_key,
                     secure=ssl,
                     region=region
                     )

    if not m_client.bucket_exists(bucket):
        m_client.make_bucket(bucket)

    return m_client


@dataclass
class InstaloaderOptions:
    instagram_username: str
    instagram_password: str


def open_instaloader(opts: InstaloaderOptions) -> Instaloader:
    loader = Instaloader(quiet=True)
    user, password = opts.instagram_username, opts.instagram_password

    try:
        loader.load_session_from_file(user, "session")
    except:
        loader.login(user, password)
        loader.save_session_to_file("session")

    return loader


@dataclass
class AMQPOptions:
    host: str = "localhost"


def open_amqp_connection(opts: AMQPOptions) -> BlockingConnection:
    # Tuple[BlockingConnection, BlockingChannel]
    params = ConnectionParameters(host=opts.host)

    connection = BlockingConnection(params)
    # channel = connection.channel()

    return connection


def open_channel(ctx: InstaminerContext, queue_name: str) -> Optional[BlockingChannel]:
    if ctx.amqp_client is None:
        return None

    channel = ctx.amqp_client.channel()
    channel.queue_declare(queue_name)

    return channel


@dataclass
class NewContextOptions:
    loader_options: InstaloaderOptions
    data_dir: str = "data/"
    queue_name: str = "instaminer"
    max_saved_memory_images: int = 10
    minio_options: Optional[MinioOptions] = None
    amqp_options: Optional[AMQPOptions] = None
    db_url: Optional[str] = None


def new_context(opts: NewContextOptions) -> InstaminerContext:
    # create data dir (if not exist)
    Path(opts.data_dir).mkdir(exist_ok=True)

    ctx = InstaminerContext(
        loader=open_instaloader(opts.loader_options),
        max_saved_memory_images=opts.max_saved_memory_images,
        last_images=defaultdict(lambda: ""),
        data_dir=opts.data_dir,
    )

    if not opts.minio_options is None:
        ctx.minio_client = open_minio(opts.minio_options)
        ctx.s3_endpoint = opts.minio_options.endpoint
        ctx.s3_bucket = opts.minio_options.bucket

    if not opts.amqp_options is None:
        ctx.amqp_client = open_amqp_connection(opts.amqp_options)
        ctx.amqp_channel = open_channel(ctx, opts.queue_name)

    if not opts.db_url is None:
        res = open_postgres_from_env(opts.db_url)

        ctx.db = res[0]
        ctx.PostModel = res[1]

    return ctx
