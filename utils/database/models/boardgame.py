from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

DeclarativeBase = declarative_base()


class BoardGame(DeclarativeBase):
    __tablename__ = 'boardgames'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    max_players = Column(Integer)

    def __repr__(self):
        return f'BoardGame(id={self.id}, name={self.name}, description={self.description}, max_players={self.max_players})'
