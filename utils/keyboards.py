from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from utils.database.models import boardgame
from typing import Type


def generate_games_keyboard(games: list[Type[boardgame.BoardGame]],
                            prefix: str = 'info', include_id: bool = False,
                            include_name: bool = False,
                            include_desc: bool = False,
                            include_max_players: bool = False) -> InlineKeyboardMarkup:
    if not (include_id or include_name or include_desc or include_max_players):
        include_name = True
    buttons = []
    i = 0
    for button_data in games:
        if i % 2 == 0:
            i = 0
            buttons.append([])
        txt = ''
        if include_id:
            txt += f'{button_data.id}\n'
        if include_name:
            txt += f'{button_data.name}\n'
        if include_desc:
            txt += f'{button_data.description}\n'
        if include_max_players:
            txt += f'{button_data.max_players}\n'
        buttons[-1].append(InlineKeyboardButton(text=txt,
                                                callback_data=f'{prefix}{button_data.id}'))
        i += 1
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def generate_id_name_get() -> ReplyKeyboardMarkup:
    # Task добавьте код создания массива из 2 кнопок с текстом 'Id' и 'Название'
    # Решение
    # Task добавьте код возвращения клавиатуры
    return # Решение
