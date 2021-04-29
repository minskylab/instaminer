from peewee import PrimaryKeyField
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
        id = PrimaryKeyField()
        date = DateField()
        hashtags = CharField()
        mentions = CharField()
        image_uri = CharField()
        likes = IntegerField()
        comments = IntegerField()
        relevance = FloatField()
        description = CharField()
        comments_content = CharField()

        class Meta:
            database = db

    return PostModel
