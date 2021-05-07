from .core import InstaminerContext, open_channel
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ChannelClosed
from entities.post import InstaminerPost
from loguru import logger


def _emit(ctx: InstaminerContext, event: str, post: InstaminerPost, max_trials: int = 3, trials: int = 0) -> None:
    if trials > max_trials:
        return

    if ctx.amqp_channel is None:
        ctx.amqp_channel = open_channel(ctx)

    try:
        if ctx.amqp_channel is None:
            return

        body = post.json()
        ctx.amqp_channel.basic_publish("", event, body)

    except BaseException as e:
        ctx.amqp_channel = open_channel(ctx)

        msg = f"error at try to emit to amqp broker, trying again [id={post.id}] [try={trials}] [error={e}]."
        logger.warning(msg)

        return _emit(ctx, event, post, max_trials, trials+1)

    return


def send_new_post(ctx: InstaminerContext, post: InstaminerPost) -> None:
    return _emit(ctx, ctx.new_post_name, post)


def send_updated_post(ctx: InstaminerContext, post: InstaminerPost) -> None:
    return _emit(ctx, ctx.new_post_update_name, post)
