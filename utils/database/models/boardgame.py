from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Task добавьте код создания экземпляра базовой структуры
DeclarativeBase=# Решение


class BoardGame(DeclarativeBase):
    # Task добавьте код присваивания имени таблицы значение 'boardgames'
    __tablename__ = 'boardgames'

    # Task добавьте код полей записи: id, целое, primary_key; name, строка; description, строка; max_players, число

    # Решение
    # Решение
    # Решение
    # Решение

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
