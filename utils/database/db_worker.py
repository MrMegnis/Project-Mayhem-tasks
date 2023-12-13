from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models.boardgame import BoardGame
from settings import get_settings
from ..logger import logger

settings = get_settings('.env')


class DBWorker:
    def __init__(self, db_path=None):
        self.session: Session | None = None
        if db_path is None:
            self.engine = create_engine(f'{settings.database.path}/{settings.database.board_games}')
        else:
            self.engine = create_engine(db_path)

    def start_session(self):
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self):
        self.session.close()

    @staticmethod
    def with_session(func):
        def wrapper(*args, **kwargs):
            self: DBWorker = args[0]
            self.start_session()
            res = func(*args, **kwargs)
            self.close_session()

        return wrapper

    @with_session
    def add_boardgame(self, name: str, description: str = None, max_players: int = None) -> bool:
        # True - successfully, False - failed
        if self.get_boardgame(name):
            logger.info(f'Board game is already in the table')
            return False
        boardgame = BoardGame(name, description, max_players)
        self.session.add(boardgame)
        self.session.commit()
        logger.info(f'Board game {name} successfully added to database!')
        return True

    @with_session
    def get_boardgame(self, name: str):
        return self.session.query(BoardGame).filter_by(name=name).first()

    @with_session
    def get_all_boardgames(self):
        pass

    @with_session
    def update_boardgame(self, boardgame_id, description: str, max_players: int):
        self.session.query(BoardGame).filter_by(id=boardgame_id).update(
            {BoardGame.description: description, BoardGame.max_players: max_players})
        self.session.commit()
        logger.info(
            f'Board game with id: {boardgame_id} updated max amount of players to {max_players} and description to {description}')

    @with_session
    def remove_boardgame(self, name):
        self.session.query(BoardGame).filter_by(name=name).delete()
        self.session.commit()
