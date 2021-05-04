from core.procedure import SearchConfigurations
from core.core import NewContextOptions, new_context, open_amqp_connection
from core.looper import looper
from settings import instaloader_options_from_env, minio_options_from_env, postgres_options_from_env, amqp_options_from_env
from asyncio import run
from datetime import datetime


opts = NewContextOptions(
    loader_options=instaloader_options_from_env(),
    minio_options=minio_options_from_env(),
    db_url=postgres_options_from_env(),
    amqp_options=amqp_options_from_env(),
    max_saved_memory_images=5,
)


ctx = new_context(opts)

run(looper(ctx, SearchConfigurations(
    query="cusco",
    delay_seconds=60*5,  # each 5min
    period_seconds=60*5,
)))
