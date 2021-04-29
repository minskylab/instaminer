
from typing import Optional
from .post import InstaminerPost
from peewee import Model


def save_instaminer_post(p: InstaminerPost, PostModel: Model) -> Optional[InstaminerPost]:
    post = PostModel(
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

    try:
        post.save()
    except BaseException as e:
        print(e)
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
