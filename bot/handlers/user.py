import logging

import settings

from aiogram import Router, Bot
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from utils.database import db_worker

bot = Bot(token=settings.get_settings('.env').bots.bot_token, parse_mode=ParseMode.HTML)
rt = Router()


class AddState(StatesGroup):
    wait_name = State()
    wait_desc = State()
    wait_max_players = State()


@rt.message(Command('start'))
async def handler_start(msg: Message):
    await msg.reply('Привет, я бот по настольным играм!')


@rt.message(Command('help'))
async def handler_help(msg: Message):
    await msg.reply('I can\'t help you')


@rt.message(Command('get_all'))
async def handler_get_all(msg: Message):
    pass


@rt.message(Command('get'))
async def handler_get(msg: Message):
    pass


@rt.message(Command('add'))
async def handler_add(msg: Message, state: FSMContext):
    await msg.reply('Введите название игры')
    await state.set_state(AddState.wait_name)


@rt.message(StateFilter(AddState.wait_name))
async def handler_name_state(msg: Message, state: FSMContext):
    await msg.reply('Введите описание игры')
    await state.update_data(game_name=msg.text)
    await state.set_state(AddState.wait_desc)


@rt.message(StateFilter(AddState.wait_desc))
async def handler_desc_state(msg: Message, state: FSMContext):
    await msg.reply('Введите максимальное количество игроков')
    await state.update_data(game_desc=msg.text)
    await state.set_state(AddState.wait_max_players)


@rt.message(StateFilter(AddState.wait_max_players))
async def handler_max_player_state(msg: Message, state: FSMContext):
    if not msg.text.isnumeric():
        await msg.reply('Количество игроков должно быть числом! Повторите ввод!')
    else:
        try:
            gd = await state.get_data()
            name, desc, mx = gd.get('game_name'), gd.get('game_desc'), msg.text
            if db_worker.DBWorker.add_boardgame(name, desc, mx):
                await msg.answer('Успешно добавлено!')
            else:
                await msg.answer('Игра уже в таблице!')
            await state.set_state()
        except Exception as _ex:
            await msg.answer('Error!')
            await state.set_state()
            logging.info(f'ERROR: {_ex}')


@rt.message(Command('delete'))
async def handler_delete(msg: Message):
    pass
