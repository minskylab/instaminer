from core.context import InstaminerContext
from typing import Optional

from loguru import logger
from peewee import Model, PostgresqlDatabase

from entities.post import InstaminerPost


def exists_instaminer_post(ctx: InstaminerContext, p: InstaminerPost) -> Optional[InstaminerPost]:
    if ctx.db_connection is None or ctx.PostModel is None:
        return None

    if ctx.db_connection.connect(True):
        logger.warning("db reconnected")

    post: Optional[Model] = None

    try:
        post = ctx.PostModel.get_by_id(p.id)
    except BaseException as e:
        post = None

    if post is not None:
        return InstaminerPost(**(post.__dict__["__data__"]))

    return None


def save_instaminer_post(ctx: InstaminerContext, p: InstaminerPost) -> Optional[InstaminerPost]:
    # TODO: FIX THIS SHIT
    if ctx.db_connection is None or ctx.PostModel is None:
        return None

    if ctx.db_connection.connect(True):
        logger.warning("db reconnected")

    post: Optional[Model] = None

    try:
        post = ctx.PostModel.get_by_id(p.id)
    except BaseException as e:
        post = None

    if post is not None:
        return InstaminerPost(**(post.__dict__["__data__"]))

    payload = dict(
        id=p.id,
        date=p.date,
        hashtags=p.hashtags,
        mentions=p.mentions,
        image_uri=p.image_uri,
        likes=p.likes,
        comments=p.comments,
        relevance=p.relevance,
        description=p.description,
        comments_content=p.comments_content,
    )

    # Bulshit
    try:
        post = ctx.PostModel.create(**payload)
    except BaseException as e:
        logger.warning(e)

        try:
            post = ctx.PostModel(**payload).save()
        except BaseException as e:
            logger.error(e)
        finally:
            return None

    return InstaminerPost(
        id=post.id,
        date=post.date,
        hashtags=post.hashtags,
        mentions=post.mentions,
        image_uri=post.image_uri,
        likes=post.likes,
        comments=post.comments,
        relevance=post.relevance,
        description=post.description,
        comments_content=post.comments_content,
    )
