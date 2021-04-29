from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import dropwhile, takewhile
from os.path import join
from typing import List, Optional

from peewee import Model

from entities.post import InstaminerPost
from instaloader import Hashtag
from instaloader.instaloader import Post

from .basic_relevance import basic_relevance
from .core import InstaminerContext
from .structures import RelevanceFunction, SearchResult

from loguru import logger


@dataclass
class SearchConfigurations:
    query: str

    delay_seconds: int = 10
    period_seconds: int = 10


@dataclass
class ProcessPostOptions:
    relevance: RelevanceFunction = basic_relevance
    folder_name: str = "laciudadinvisible"


def search_by_hashtag(ctx: InstaminerContext, opts: SearchConfigurations, process_opts: ProcessPostOptions = ProcessPostOptions()) -> SearchResult:
    posts = Hashtag.from_name(ctx.loader.context, opts.query).get_posts()

    since = datetime.now() - timedelta(seconds=opts.delay_seconds+opts.period_seconds)
    until = since + timedelta(seconds=opts.period_seconds)

    logger.info(f"searching interval: {since} - {until}")

    for post in takewhile(lambda p: p.date_local > since, dropwhile(lambda p: p.date_local > until, posts)):
        i_post = process_post(ctx, post, process_opts)

        if i_post is None:
            continue

        yield i_post


def process_post(ctx: InstaminerContext, post: Post, opts: ProcessPostOptions) -> Optional[InstaminerPost]:
    likes = post.likes
    comments = post.comments
    date = post.date_local
    _id = post.shortcode

    rel = opts.relevance(likes, comments)  # type: ignore

    msg = f"post found [id={_id}] | L: {likes}, C: {comments}, D: {date}, R: {rel}"
    logger.info(msg)

    filepath = join(ctx.data_dir, post.shortcode)

    post_x: Optional[Model] = True

    if ctx.PostModel is not None:
        try:
            post_x = ctx.PostModel.get_by_id(_id)
        except BaseException as e:
            post_x = None

    if post_x is not None:
        return InstaminerPost(**(post_x.__dict__["__data__"]))

    try:
        ctx.loader.download_pic(filepath, post.url, post.date)
    except BaseException as e:
        logger.warning(e)

    link: str = filepath

    if ctx.minio_client is not None:
        bucket = ctx.s3_bucket
        endpoint = ctx.s3_endpoint
        folder_name = opts.folder_name

        destination = folder_name + "/" + post.shortcode + ".jpg"

        full_filepath = filepath + ".jpg"

        try:
            ctx.minio_client.fput_object(bucket,
                                         destination,
                                         full_filepath,
                                         content_type="image/jpg",
                                         metadata={"x-amz-acl": "public-read"})

            link = f"https://{bucket}.{endpoint}/{destination}"
        except BaseException as e:
            logger.warning(e)

    full_comments: List[str] = []

    for comment in post.get_comments():
        full_comments.append(str(comment))

    return InstaminerPost(
        id=post.shortcode,
        date=post.date_local,
        likes=post.likes,
        comments=post.comments,
        hashtags=",".join(post.caption_hashtags),
        mentions=",".join(post.caption_mentions),
        relevance=rel,
        image_uri=link,
        description=post.caption,
        comments_content=",".join(full_comments),
    )
