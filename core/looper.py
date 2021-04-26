

from core.procedure import SearchConfigurations, search_by_hashtag
from .core import InstaminerContext
from asyncio import sleep


async def search_tick(ctx: InstaminerContext, config: SearchConfigurations):
    for res in search_by_hashtag(ctx, config):
        print(res)


async def looper(ctx: InstaminerContext, config: SearchConfigurations):
    while True:
        await search_tick(ctx, config)
        await sleep(config.period_seconds)
