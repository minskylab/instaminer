from os import getenv

from core.options import AMQPOptions, InstaloaderOptions, MinioOptions
from dotenv import load_dotenv

load_dotenv()


def minio_options_from_env() -> MinioOptions:
    # load_dotenv()

    ssl: bool = True

    if isinstance(ssl_env := getenv("S3_SSL", True), str):
        ssl = (ssl_env.lower() in ['true', '1', 't', 'y', 'yes'])

    return MinioOptions(
        endpoint=getenv("S3_ENDPOINT", ""),
        access_key=getenv("S3_ACCESS_KEY", ""),
        secret_key=getenv("S3_SECRET_KEY", ""),
        bucket=getenv("S3_BUCKET", ""),
        ssl=ssl,
        region=getenv("S3_REGION", ""),
    )


def instaloader_options_from_env() -> InstaloaderOptions:
    # load_dotenv()

    return InstaloaderOptions(
        instagram_username=getenv("IG_USERNAME", ""),
        instagram_password=getenv("IG_PASSWORD", ""),
    )


def postgres_options_from_env() -> str:
    # load_dotenv()

    return getenv("DB_URL", "")


def amqp_options_from_env() -> AMQPOptions:
    # load_dotenv()

    return AMQPOptions(
        host=getenv("AMQP_HOST", "localhost")
    )