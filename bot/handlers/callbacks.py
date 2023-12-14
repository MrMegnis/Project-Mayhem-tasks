from aiogram.types import CallbackQuery
from utils.database import db_worker
from user import rt


@rt.callback_query()
async def callbacks(call: CallbackQuery):
    if call.data[:4] == 'info':
        game_id = call.data[4:]
        game = db_worker.DBWorker.get_boardgame_by_id(int(game_id))
        if game is None:
            await call.answer('Игра не существует!')
        else:
            await call.answer(f'id: {game.id}\n'
                              f'Название: {game.name}\n'
                              f'Описание: {game.description}\n'
                              f'Максимальное количество игроков: {game.max_players}')

