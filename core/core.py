from collections import defaultdict
from database.new import open_postgres_from_env_v2
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from instaloader.instaloader import Instaloader
from minio import Minio
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from core.garbage_collector import purge_all_data_dir

from .context import InstaminerContext
from .options import AMQPOptions, InstaloaderOptions, MinioOptions

from loguru import logger


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


def open_anonymous_instaloader() -> Instaloader:
    loader = Instaloader(quiet=True)
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
    data_dir: str = "data/"
    queue_name: str = "instaminer"
    max_saved_memory_images: int = 10
    loader_options: Optional[InstaloaderOptions] = None
    minio_options: Optional[MinioOptions] = None
    amqp_options: Optional[AMQPOptions] = None
    db_url: Optional[str] = None


async def new_context(opts: NewContextOptions) -> InstaminerContext:
    # create data dir (if not exist)
    Path(opts.data_dir).mkdir(exist_ok=True)

    loader: Optional[Instaloader] = None

    if opts.loader_options is None:
        loader = open_anonymous_instaloader()
        logger.warning("instagram anonymous session activated.")
    else:
        loader = open_instaloader(opts.loader_options)

    ctx = InstaminerContext(
        loader=loader,
        last_images=defaultdict(lambda: ""),
        max_saved_memory_images=opts.max_saved_memory_images,
        data_dir=opts.data_dir,
        queue_name=opts.queue_name,
        amqp_options=opts.amqp_options,
        db_url=opts.db_url,
    )

    if not opts.minio_options is None:
        ctx.minio_client = open_minio(opts.minio_options)
        ctx.s3_endpoint = opts.minio_options.endpoint
        ctx.s3_bucket = opts.minio_options.bucket

    if not opts.amqp_options is None:
        ctx.amqp_connection = open_amqp_connection(opts.amqp_options)
        ctx.amqp_channel = open_channel(ctx)

    if not opts.db_url is None:
        ctx.db_connection = await open_postgres_from_env_v2(opts.db_url)
        pass

    purge_all_data_dir(ctx)

    return ctx
