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
            self.engine = create_engine(db_path)

    def start_session(self) -> None:
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self) -> None:
        self.session.close()

    @staticmethod
    def with_session(func):
        def wrapper(*args, **kwargs):
            self: DBWorker = args[0]
            self.start_session()
            DeclarativeBase.metadata.create_all(self.engine)
            res = func(*args, **kwargs)
            self.close_session()
            return res

        return wrapper

    @with_session
    def add_boardgame(self, name: str, description: str = None, max_players: int = None) -> None:
        if self.get_boardgames_by_extra_fields(name, description, max_players):
            logger.info(f'Board game with the same fields is already in the table')
        self.session.add(BoardGame(name=name, description=description, max_players=max_players))
        self.session.commit()
        logger.info(f'Board game {name} successfully added to database!')

    @with_session
    def get_boardgame_by_id(self, boardgame_id: int) -> BoardGame | None:
        return self.session.query(BoardGame).filter_by(id=boardgame_id).first()

    @with_session
    def get_boardgames_by_extra_fields(self, name: str = None, description: str = None,
                                       max_players: int = None) -> list[Type[BoardGame]]:
        return (self.session.query(BoardGame)
                .filter(BoardGame.name == name if name is not None else True)
                .filter(BoardGame.description == description if description is not None else True)
                .filter(BoardGame.max_players == max_players if max_players is not None else True).all())

    @with_session
    def remove_boardgame_by_id(self, boardgame_id: int) -> None:
        self.session.query(BoardGame).filter_by(id=boardgame_id).delete()
        self.session.commit()

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
        return self.session.query(BoardGame).all()
