from typing import Union
from dotenv import load_dotenv
from core.core import InstaloaderOptions, MinioOptions
from os import getenv


def minio_options_from_env() -> MinioOptions:
    load_dotenv()

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


def instaloader_from_env() -> InstaloaderOptions:
    load_dotenv()

    return InstaloaderOptions(
        instagram_username=getenv("IG_USERNAME", ""),
        instagram_password=getenv("IG_PASSWORD", ""),
    )


def postgres_from_env() -> str:
    load_dotenv()

    return getenv("DB_URL", "")
