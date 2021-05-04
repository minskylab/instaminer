from .core import InstaminerContext
from pika.adapters.blocking_connection import BlockingChannel
from entities.post import InstaminerPost
from loguru import logger


def _emit(event: str, channel: BlockingChannel, post: InstaminerPost) -> None:
    try:
        channel.basic_publish(exchange='', routing_key=event, body=post.json())
    except BaseException as e:
        msg = f"error at try to emit to amqp broker [id={post.id}], [error={e}]"
        logger.error(msg)


def send_new_post(ctx: InstaminerContext, post: InstaminerPost) -> None:
    # ctx.amqp_client.
    return _emit(ctx.new_post_name, ctx.amqp_channel, post)


def send_updated_post(ctx: InstaminerContext, post: InstaminerPost) -> None:
    return _emit(ctx.new_post_update_name, ctx.amqp_channel, post)
