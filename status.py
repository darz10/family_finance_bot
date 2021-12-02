from aiogram.dispatcher.filters.state import State, StatesGroup


class OwnerStatus(StatesGroup):
    """Статусы меню"""

    no_access = State()
    unregistred = State()
    in_main_menu = State()
    in_family_finance_menu = State()
    in_my_finance_menu = State()
    in_menu_choice_action = State()
    in_view_situation_menu = State()
    in_fill_data_menu = State()
    in_record_data_menu = State()
