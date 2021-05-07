from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from loguru import logger

from database import open_postgres_from_env
from instaloader.instaloader import Instaloader
from minio import Minio
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from core.garbage_collector import drain_images

from .context import InstaminerContext
from .options import AMQPOptions, InstaloaderOptions, MinioOptions


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


def open_instaloader(opts: InstaloaderOptions) -> Instaloader:
    loader = Instaloader(quiet=True)
    user, password = opts.instagram_username, opts.instagram_password

    try:
        loader.load_session_from_file(user, "session")
    except:
        loader.login(user, password)
        loader.save_session_to_file("session")

    return loader


def open_amqp_connection(opts: AMQPOptions) -> BlockingConnection:
    # Tuple[BlockingConnection, BlockingChannel]
    params = ConnectionParameters(host=opts.host)
    connection = BlockingConnection(params)
    # channel = connection.channel()

    return connection


def open_channel(ctx: InstaminerContext) -> Optional[BlockingChannel]:
    if ctx.amqp_options is None:
        return None

    if ctx.amqp_connection is not None and ctx.amqp_connection.is_closed:
        ctx.amqp_connection = open_amqp_connection(ctx.amqp_options)

    if ctx.amqp_connection is None:
        return None

    channel = ctx.amqp_connection.channel()
    channel.queue_declare(ctx.queue_name)

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

    loader = open_instaloader(opts.loader_options)

    ctx = InstaminerContext(
        loader=loader,
        last_images=defaultdict(lambda: ""),
        max_saved_memory_images=opts.max_saved_memory_images,
        data_dir=opts.data_dir,
        queue_name=opts.queue_name,
        amqp_options=opts.amqp_options,
    )

    if not opts.minio_options is None:
        ctx.minio_client = open_minio(opts.minio_options)
        ctx.s3_endpoint = opts.minio_options.endpoint
        ctx.s3_bucket = opts.minio_options.bucket

    if not opts.amqp_options is None:
        ctx.amqp_connection = open_amqp_connection(opts.amqp_options)
        ctx.amqp_channel = open_channel(ctx)

    if not opts.db_url is None:
        res = open_postgres_from_env(opts.db_url)

        ctx.db = res[0]
        ctx.PostModel = res[1]

    drain_images(ctx)

    return ctx
