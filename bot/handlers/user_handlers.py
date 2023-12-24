import logging

import settings

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.enums.parse_mode import ParseMode
from utils.database.db_worker import DBWorker
from utils import keyboards
from bot.handlers.states import StateClass

rt = Router()
db_worker = DBWorker()


@rt.message(Command('start'))
async def handler_start(msg: Message):
    # Task добавьте код ответа на сообщение с текстом 'Привет, я бот по настольным играм!'
    # Решение
    await handler_help(msg)


@rt.message(Command('help'))
async def handler_help(msg: Message):
    answer_text = '/get_all - получить все игры\n/get - получить игру по id или названию\n/add - добавить новую игру\n/delete - удалить игру по id или названию'
    # Task добавьте код ответа на сообщение с текстом из answer_text
    # Решение


@rt.message(Command('get_all'))
async def handler_get_all(msg: Message):
    try:
        games_list = db_worker.get_all_boardgames()
        if len(games_list) == 0:
            # Task добавьте код ответа на сообщение с текстом 'В базе данных пока нет игр'
            # Решение
            return
        keyboard = keyboards.generate_games_keyboard(games_list, include_name=True)
        answer_text = 'Список всех игр:\nДля получения подробной информации нажмите на кнопку'
        # Task добавьте код ответа на сообщение с текстом из answer_text и клавиатурой keyboard
        # Решение
    except Exception as _ex:
        logging.info(f'ERROR: {_ex}')
        await msg.reply('ERROR!')


@rt.message(Command('get'))
async def handler_get(msg: Message, state: FSMContext):
    keyboard = keyboards.generate_id_name_get()
    answer_text = 'Список всех игр:\nДля получения подробной информации нажмите на кнопку'
    # Task добавьте код ответа на сообщение с текстом из answer_text и клавиатурой keyboard
    # Решение
    # Task добавьте код установки состояния на StateClass.get_wait_parameter
    # Решение


@rt.message(StateFilter(StateClass.get_wait_parameter))
async def handler_get_state(msg: Message, state: FSMContext):
    pass
    if msg.text == 'Id':
        pass
        # Task добавьте код ответа на сообщение с текстом 'Введите Id' и клавиатурой ReplyKeyboardRemove()
        # Решение
        # Task добавьте код установки состояния на StateClass.get_wait_id
        # Решение
    elif msg.text == 'Название':
        pass
        # Task добавьте код ответа на сообщение с текстом 'Введите название' и клавиатурой ReplyKeyboardRemove()
        # Решение
        # Task добавьте код установки состояния на StateClass.get_wait_name
        # Решение
    else:
        pass
        # Task добавьте код ответа на сообщение с текстом 'Неправильный параметр!' и клавиатурой ReplyKeyboardRemove()
        # Решение
        # Task добавьте код установки состояния на начальное
        # Решение


@rt.message(StateFilter(StateClass.get_wait_id))
async def handler_id_get_state(msg: Message, state: FSMContext):
    try:
        if not msg.text.isnumeric():
            await msg.reply('Id должен быть числом!')
        else:
            game = db_worker.get_boardgame_by_id(int(msg.text))
            if game is None:
                await msg.reply('Игры с таким id не существует!')
            else:
                await msg.reply(f'id: {game.id}\n'
                                f'Название: {game.name}\n'
                                f'Описание: {game.description}\n'
                                f'Максимальное количество игроков: {game.max_players}')
    except Exception as _ex:
        logging.info(f'ERROR: {_ex}')
        await msg.reply('ERROR!')
    finally:
        await state.set_state()


@rt.message(StateFilter(StateClass.get_wait_name))
async def handler_name_get_state(msg: Message, state: FSMContext):
    try:
        games = db_worker.get_boardgames_by_extra_fields(name=msg.text)
        if len(games) == 0:
            await msg.reply('Игр с таким названием не существует!')
        else:
            keyboard = keyboards.generate_games_keyboard(games, include_id=True)
            await msg.reply('Вот id игр с этим именем\n'
                            'Для получения подробностей нажмите на кнопку',
                            reply_markup=keyboard)

    except Exception as _ex:
        logging.info(f'ERROR: {_ex}')
        await msg.reply('ERROR!')
    finally:
        await state.set_state()


@rt.message(Command('add'))
async def handler_add(msg: Message, state: FSMContext):
    await msg.reply('Введите название игры')
    await state.set_state(StateClass.add_wait_name)


@rt.message(StateFilter(StateClass.add_wait_name))
async def handler_name_state(msg: Message, state: FSMContext):
    await msg.reply('Введите описание игры')
    await state.update_data(game_name=msg.text)
    await state.set_state(StateClass.add_wait_desc)


@rt.message(StateFilter(StateClass.add_wait_desc))
async def handler_desc_state(msg: Message, state: FSMContext):
    await msg.reply('Введите максимальное количество игроков')
    await state.update_data(game_desc=msg.text)
    await state.set_state(StateClass.add_wait_max_players)


@rt.message(StateFilter(StateClass.add_wait_max_players))
async def handler_max_player_state(msg: Message, state: FSMContext):
    if not msg.text.isnumeric():
        await msg.reply('Количество игроков должно быть числом! Повторите ввод!')
    else:
        try:
            gd = await state.get_data()
            name, desc, mx = gd.get('game_name'), gd.get('game_desc'), msg.text
            db_worker.add_boardgame(name, desc, mx)
            await state.set_state()
            await msg.reply('Успешно!')
        except Exception as _ex:
            await msg.answer('Error!')
            await state.set_state()
            logging.info(f'ERROR: {_ex}')


@rt.message(Command('delete'))
async def handler_delete(msg: Message, state: FSMContext):
    keyboard = keyboards.generate_id_name_get()
    await msg.reply('По какому параметру вы хотите удалить игру?\nId/Название',
                    reply_markup=keyboard)
    await state.set_state(StateClass.del_wait_parameter)


@rt.message(StateFilter(StateClass.del_wait_parameter))
async def handler_del_state(msg: Message, state: FSMContext):
    if msg.text == 'Id':
        await msg.reply('Введите Id', reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateClass.del_wait_id)
    elif msg.text == 'Название':
        await msg.reply('Введите название', reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateClass.del_wait_name)
    else:
        await msg.reply('Неправильный параметр!', reply_markup=ReplyKeyboardRemove())
        await state.set_state()


@rt.message(StateFilter(StateClass.del_wait_id))
async def handler_id_del_state(msg: Message, state: FSMContext):
    try:
        if not msg.text.isnumeric():
            await msg.reply('Id должно быть числом!')
        else:
            db_worker.remove_boardgame_by_id(int(msg.text))
            await msg.reply('Успешно!')
    except Exception as _ex:
        logging.info(f'ERROR: {_ex}')
        await msg.reply('ERROR!')
    finally:
        await state.set_state()


@rt.message(StateFilter(StateClass.del_wait_name))
async def handler_name_del_state(msg: Message, state: FSMContext):
    try:
        db_worker.remove_boardgames_by_extra_fields(name=msg.text)
        await msg.reply('Успешно!')
    except Exception as _ex:
        logging.info(f'ERROR: {_ex}')
        await msg.reply('ERROR!')
    finally:
        await state.set_state()
