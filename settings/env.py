from core.procedure import SearchConfigurations
from os import getenv
from typing import Optional

from core.options import AMQPOptions, InstaloaderOptions, MinioOptions

from .names import (amqp_hostname_name, db_url_name, delay_seconds_name,
                    instagram_password_name, instagram_user_name,
                    period_seconds_name, query_search_name, s3_access_key_name,
                    s3_bucket_name, s3_endpoint_name, s3_region_name,
                    s3_secret_key_name, s3_ssl_name)


def minio_options_from_env() -> Optional[MinioOptions]:
    endpoint: Optional[str] = getenv(s3_endpoint_name, None)
    access_key: Optional[str] = getenv(s3_access_key_name, None)
    secret_key: Optional[str] = getenv(s3_secret_key_name, None)

    bucket: str = getenv(s3_bucket_name, "instaminer")
    region: str = getenv(s3_region_name, "sfo2")

    ssl: bool = True

    if isinstance(ssl_env := getenv(s3_ssl_name, True), str):
        ssl = (ssl_env.lower() in ['true', '1', 't', 'y', 'yes'])

    if endpoint is None or access_key is None or secret_key is None:
        return None

    return MinioOptions(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        bucket=bucket,
        ssl=ssl,
        region=region,
    )


def instaloader_options_from_env() -> Optional[InstaloaderOptions]:
    ig_username: Optional[str] = getenv(instagram_user_name, None)
    ig_password: Optional[str] = getenv(instagram_password_name, None)

    if ig_username is None or ig_password is None:
        return None

    return InstaloaderOptions(
        instagram_username=ig_username,
        instagram_password=ig_password,
    )


def postgres_options_from_env() -> Optional[str]:
    return getenv(db_url_name, None)


def amqp_options_from_env() -> Optional[AMQPOptions]:
    # TODO: Close AMQP options implementation

    amqp_host: Optional[str] = getenv(amqp_hostname_name, None)

    if amqp_host is None:
        return None

    return AMQPOptions(
        host=amqp_host,
    )


def load_search_configuration() -> SearchConfigurations:
    query: Optional[str] = getenv(query_search_name, None)

    period: int = int(getenv(period_seconds_name, "300"))  # each 5min
    delay: int = int(getenv(delay_seconds_name, "300"))  # from last 5min

    if query is None or period < 0 or delay < 0:
        raise BaseException(
            "you need to define your query, delay and period correctly")

    return SearchConfigurations(
        query=query,
        period_seconds=int(period),
        delay_seconds=int(delay),
    )
