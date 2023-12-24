from aiogram.fsm.state import StatesGroup, State


class StateClass(StatesGroup):
    add_wait_name = State()
    add_wait_desc = State()
    add_wait_max_players = State()

    get_wait_parameter = State()
    get_wait_id = State()
    get_wait_name = State()

    del_wait_parameter = State()
    del_wait_id = State()
    del_wait_name = State()
