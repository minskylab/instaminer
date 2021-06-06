from typing import Optional
from entities.post import InstaminerPost
from core.context import InstaminerContext
from asyncpg import Connection, connect, Record
from loguru import logger

POST_TABLE_NAME = "postmodel"


async def open_postgres_from_env_v2(db_url: str) -> Connection:
    return await connect(db_url)


async def exists_instaminer_post_v2(ctx: InstaminerContext, p: InstaminerPost) -> Optional[InstaminerPost]:
    q = f"SELECT * FROM {POST_TABLE_NAME} WHERE id = $1"

    try:
        if ctx.db_connection is None:
            logger.error("db_connection is None")
            return None

        row: Record = await ctx.db_connection.fetchrow(q, p.id)
    except BaseException as e:
        logger.error(e)
        return None

    if row is None:
        return None

    return InstaminerPost(**dict(row))


async def save_instaminer_post_v2(ctx: InstaminerContext, p: InstaminerPost) -> Optional[InstaminerPost]:
    insertion_query = f"""
    INSERT INTO {POST_TABLE_NAME}(
        id,
        date,
        hashtags,
        mentions,
        image_uri,
        likes,
        comments,
        relevance,
        description,
        comments_content
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    """

    try:
        if ctx.db_connection is None:
            logger.error("db_connection is None")
            return None

        res = await ctx.db_connection.execute(
            insertion_query,
            p.id,
            p.date,
            p.hashtags,
            p.mentions,
            p.image_uri,
            p.likes,
            p.comments,
            p.relevance,
            p.description or "empty",
            p.comments_content,
        )

    except BaseException as e:
        logger.error(e)
        return None

    return p
