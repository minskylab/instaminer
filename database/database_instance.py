from peewee import PostgresqlDatabase


def open_postgres_from_env(db_url: str) -> PostgresqlDatabase:
    return PostgresqlDatabase(db_url)
