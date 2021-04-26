from peewee import PostgresqlDatabase
from os import getenv
from dotenv import load_dotenv


load_dotenv()

db_url = getenv("DB_URL")

db = PostgresqlDatabase(db_url)
