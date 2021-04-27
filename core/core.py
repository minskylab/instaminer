from emitter.amqp import AMQPOptions, open_amqp_connection
from pika import BlockingConnection
from dataclasses import dataclass
from typing import Optional
from minio import Minio
from instaloader.instaloader import Instaloader
from pathlib import Path


@dataclass
class InstaminerContext:
    minio_client: Minio
    loader: Instaloader
    amqp_client: BlockingConnection

    data_dir: str

    s3_endpoint: Optional[str] = None
    s3_bucket: Optional[str] = None


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
    loader = Instaloader()
    user, password = opts.instagram_username, opts.instagram_password

    try:
        loader.load_session_from_file(user, "session")
    except:
        loader.login(user, password)
        loader.save_session_to_file("session")

    return loader


@dataclass
class NewContextOptions:
    minio_options: MinioOptions
    loader_options: InstaloaderOptions
    amqp_options: AMQPOptions

    data_dir: str = "data/"


def new_context(opts: NewContextOptions) -> InstaminerContext:
    # create data dir (if not exist)
    Path(opts.data_dir).mkdir(exist_ok=True)

    return InstaminerContext(
        minio_client=open_minio(opts.minio_options),
        amqp_client=open_amqp_connection(opts.amqp_options),
        loader=open_instaloader(opts.loader_options),
        data_dir=opts.data_dir,

        s3_endpoint=opts.minio_options.endpoint,
        s3_bucket=opts.minio_options.bucket,
    )
