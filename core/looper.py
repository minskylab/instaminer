from core.emit import send_new_post
from core.garbage_collector import update_garbage_collector
from entities.post_operations import exists_instaminer_post, save_instaminer_post
from core.procedure import SearchConfigurations, search_by_hashtag
from .core import InstaminerContext
from asyncio import sleep
from loguru import logger


async def search_tick(ctx: InstaminerContext, config: SearchConfigurations):
    for post in search_by_hashtag(ctx, config):
        msg = f"post found [id={post.id}] | L: {post.likes}, C: {post.comments}, D: {post.date}, R: {round(post.relevance, 3)}"
        logger.info(msg)

        if ctx.db is not None:
            logger.debug(f"trying to save post [id={post.id}]")

            msg = f"error at try to resolve found post [id={post.id}]"

            if exists_instaminer_post(post, ctx.PostModel) is not None:
                msg = f"found post [id={post.id}] into DB [name={ctx.db.database}]"
            elif save_instaminer_post(post, ctx.PostModel) is not None:
                msg = f"created post [id={post.id}] into DB [name={ctx.db.database}]"

            logger.debug(msg)

        if ctx.amqp_client is not None and ctx.amqp_channel is not None:
            logger.debug(f"sending to amqp broker")
            send_new_post(ctx, post)


async def looper(ctx: InstaminerContext, config: SearchConfigurations):
    while True:
        await search_tick(ctx, config)
        await sleep(config.period_seconds)
