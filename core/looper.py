from entities.post_operations import exists_instaminer_post, save_instaminer_post
from core.procedure import SearchConfigurations, search_by_hashtag
from .core import InstaminerContext
from asyncio import sleep
from loguru import logger


async def search_tick(ctx: InstaminerContext, config: SearchConfigurations):
    for post in search_by_hashtag(ctx, config):
        if ctx.db is not None:
            logger.info(f"trying to save post [id={post.id}]")

            msg = f"error at try to resolve found post [id={post.id}]"

            if exist_post := exists_instaminer_post(post, ctx.PostModel) is not None:
                msg = f"found post [id={post.id}] into DB [name={ctx.db.database}]"
            elif created_post := save_instaminer_post(post, ctx.PostModel) is not None:
                msg = f"created post [id={post.id}] into DB [name={ctx.db.database}]"

            logger.info(msg)


async def looper(ctx: InstaminerContext, config: SearchConfigurations):
    while True:
        await search_tick(ctx, config)
        await sleep(config.period_seconds)
