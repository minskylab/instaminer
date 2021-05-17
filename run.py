from core.procedure import SearchConfigurations
from core.core import NewContextOptions, new_context
from core.looper import looper
from settings import instaloader_options_from_env, minio_options_from_env, postgres_options_from_env, amqp_options_from_env
from asyncio import run


opts = NewContextOptions(
    loader_options=instaloader_options_from_env(),
    minio_options=minio_options_from_env(),
    db_url=postgres_options_from_env(),
    max_saved_memory_images=5,
    # amqp_options=amqp_options_from_env(),
)


ctx = new_context(opts)

run(looper(ctx, SearchConfigurations(
    query="cusco",
    delay_seconds=5*60,  # each 5min
    period_seconds=5*60,
)))
