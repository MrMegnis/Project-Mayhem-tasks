from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str


@dataclass
class Database:
    path: str


@dataclass
class Settings:
    bots: Bots
    database: Database


def get_settings(path: str) -> Settings:
    load_dotenv(path)

    return Settings(
        bots=Bots(
            bot_token=getenv('BOT_TOKEN')
        ),
        database=Database(
            path=f"{getenv('DB_ADAPTER')}://{getenv('DB_USER')}:{getenv('DB_USER_PASSWORD')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}",
        )
    )
