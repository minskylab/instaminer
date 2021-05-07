from peewee import DateTimeField, Model, CharField, IntegerField, FloatField, TextField
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from peewee import PostgresqlDatabase


class InstaminerPost(BaseModel):
    id: str
    date: datetime
    hashtags: str
    mentions: str
    image_uri: str
    likes: int
    comments: int
    relevance: float
    description: Optional[str]
    comments_content: Optional[str]


def define_post_model(db: PostgresqlDatabase) -> Model:
    class PostModel(Model):
        id = CharField(primary_key=True)
        date = DateTimeField()
        hashtags = TextField()
        mentions = TextField()
        image_uri = TextField()
        likes = IntegerField()
        comments = IntegerField()
        relevance = FloatField()
        description = TextField()
        comments_content = TextField()

        class Meta:
            database = db

    return PostModel
