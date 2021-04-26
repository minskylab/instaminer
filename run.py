
from core.procedure import SearchConfigurations
from core.core import NewContextOptions, new_context
from core.looper import looper
from settings import instaloader_from_env, minio_options_from_env
from asyncio import run

opts = NewContextOptions(
    minio_options=minio_options_from_env(),
    loader_options=instaloader_from_env())


ctx = new_context(opts)

run(looper(ctx, SearchConfigurations(
    query="cusco",
    delay_seconds=60,
    period_seconds=60,
)))
