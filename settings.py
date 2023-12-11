from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str) -> Settings:
    load_dotenv(path)

    return Settings(
        bots=Bots(
            bot_token=getenv('BOT_TOKEN')
        )
    )
