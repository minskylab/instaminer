from peewee import Model
from typing import Tuple
from entities.post import define_post_model
from peewee import PostgresqlDatabase
from urllib.parse import urlparse


def open_postgres_from_env(db_url: str) -> Tuple[PostgresqlDatabase, Model]:
    url = urlparse(db_url)

    if url.scheme != "postgres":
        raise BaseException("invalid db_url schema")

    chunks = url.netloc.split("@")

    cred, host_p = chunks[0], chunks[1]

    cred_arr = cred.split(":")
    host_p_arr = host_p.split(":")

    db = PostgresqlDatabase(url.path.replace("/", ""),
                            host=host_p_arr[0],
                            port=host_p_arr[1],
                            user=cred_arr[0],
                            password=cred_arr[1],
                            )
    PostModel = define_post_model(db)

    db.connect()
    db.create_tables([PostModel])

    return db, PostModel
