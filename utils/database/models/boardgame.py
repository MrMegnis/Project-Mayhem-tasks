from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DeclarativeBase = declarative_base()


class BoardGame(DeclarativeBase):
    __tablename__ = 'boardgames'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    max_players = Column(Integer)

    def __repr__(self):
        return f'BoardGame(id={self.id}, name={self.name}, description={self.description}, max_players={self.max_players})'


def wipe_boardgames_table():
    from settings import get_settings

    settings = get_settings('../../../.env')

    engine = create_engine(f'{settings.database.path}')
    session_class = sessionmaker(bind=engine)
    db_session = session_class()

    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)
    db_session.commit()
    db_session.close()
    print('users wiped!')


if __name__ == '__main__':
    wipe_boardgames_table()
