from core.core import InstaminerContext
from pika.adapters.blocking_connection import BlockingChannel
from entities.post import InstaminerPost


new_post_name = "new_post"
new_post_update = "updated_post"


def open_channel(ctx: InstaminerContext, queue_name: str) -> BlockingChannel:
    channel = ctx.amqp_client.channel()
    channel.queue_declare(queue_name)


def _emit(event: str, channel: BlockingChannel, post: InstaminerPost) -> None:
    channel.basic_publish(exchange='', routing_key=event, body=post.json())


def send_new_post(channel: BlockingChannel, post: InstaminerPost) -> None:
    return _emit(new_post_name, channel, post)


def send_updated_post(channel: BlockingChannel, post: InstaminerPost) -> None:
    return _emit(new_post_update, channel, post)
