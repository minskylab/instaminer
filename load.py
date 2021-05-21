
from settings.env import amqp_options_from_env, instaloader_options_from_env, minio_options_from_env, postgres_options_from_env
from core.core import NewContextOptions


def default_context_options() -> NewContextOptions:
    loader_options = instaloader_options_from_env()

    # if loader_options is None:

    # raise BaseException(
    #     "we need a instagram credentials for an authorized session")

    return NewContextOptions(
        loader_options=loader_options,
        minio_options=minio_options_from_env(),
        db_url=postgres_options_from_env(),
        amqp_options=amqp_options_from_env(),
    )
