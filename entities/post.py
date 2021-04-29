from peewee import Model, PrimaryKeyField, DateField, CharField, IntegerField, FloatField
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from peewee import PostgresqlDatabase


class InstaminerPost(BaseModel):
    id: str
    date: datetime
    hashtags: List[str]
    mentions: List[str]
    image_uri: str
    likes: int
    comments: int
    relevance: float
    description: Optional[str]
    comments_content: Optional[List[str]]


def define_post_model(db: PostgresqlDatabase) -> Model:
    class PostModel(Model):
        id = CharField(primary_key=True)
        date = DateField()
        hashtags = CharField(max_length=10000)
        mentions = CharField(max_length=10000)
        image_uri = CharField(max_length=10000)
        likes = IntegerField()
        comments = IntegerField()
        relevance = FloatField()
        description = CharField(max_length=10000)
        comments_content = CharField(max_length=10000)

        class Meta:
            database = db

    return PostModel
