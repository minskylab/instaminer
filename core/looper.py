

from entities.post_operations import save_instaminer_post
from core.procedure import SearchConfigurations, search_by_hashtag
from .core import InstaminerContext
from asyncio import sleep


async def search_tick(ctx: InstaminerContext, config: SearchConfigurations):
    for post in search_by_hashtag(ctx, config):

        print(ctx.db, ctx.PostModel)

        if ctx.db is not None:
            print("saving post")
            created_post = save_instaminer_post(post, ctx.PostModel)
            if created_post is not None:
                print(created_post)


async def looper(ctx: InstaminerContext, config: SearchConfigurations):
    while True:
        await search_tick(ctx, config)
        await sleep(config.period_seconds)
