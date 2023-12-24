from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from utils.database.models.boardgame import BoardGame, DeclarativeBase
from settings import get_settings
from utils.logger import logger

settings = get_settings('.env')


class DBWorker:
    def __init__(self, db_path: str = None) -> None:
        self.session: Session | None = None
        if db_path is None:
            self.engine = create_engine(f'{settings.database.path}')
        else:
            pass
            # Task добавьте код создания engine для бд с ссылкой на бд в db_path
            # Решение

    def start_session(self) -> None:
        pass
        # Task добавьте код создания сессии
        # Решение

    def close_session(self) -> None:
        self.session.close()

    @staticmethod
    def with_session(func):
        def wrapper(*args, **kwargs):
            self: DBWorker = args[0]
            self.start_session()
            # Task добавьте код создания всех таблиц
            # Решение
            res = func(*args, **kwargs)
            self.close_session()
            return res

        return wrapper

    @with_session
    def add_boardgame(self, name: str, description: str = None, max_players: int = None) -> None:
        if self.get_boardgames_by_extra_fields(name, description, max_players):
            logger.info(f'Board game with the same fields is already in the table')
        # Task добавьте код добавления записи игры в таблицу
        # Решение
        # Решение
        logger.info(f'Board game {name} successfully added to database!')

    @with_session
    def get_boardgame_by_id(self, boardgame_id: int) -> BoardGame | None:
        # Task добавьте код получения записи по id
        return # Решение

    @with_session
    def get_boardgames_by_extra_fields(self, name: str = None, description: str = None,
                                       max_players: int = None) -> list[Type[BoardGame]]:
        return (self.session.query(BoardGame)
                .filter(BoardGame.name == name if name is not None else True)
                .filter(BoardGame.description == description if description is not None else True)
                .filter(BoardGame.max_players == max_players if max_players is not None else True).all())

    @with_session
    def remove_boardgame_by_id(self, boardgame_id: int) -> None:
        pass
        # Task добавьте код удаления записи по id
        # Решение
        # Решение

    @with_session
    def remove_boardgames_by_extra_fields(self, name: str = None, description: str = None,
                                          max_players: int = None) -> None:
        (self.session.query(BoardGame)
         .filter(BoardGame.name == name if name is not None else True)
         .filter(BoardGame.description == description if description is not None else True)
         .filter(BoardGame.max_players == max_players if max_players is not None else True).delete())
        self.session.commit()

    @with_session
    def get_all_boardgames(self) -> list[Type[BoardGame]]:
        # Task добавьте код получения всех записей
        return # Решение
