from typing import Union
from datetime import datetime

from aiogram import types

from constants import Action
import database.query as db
from status import OwnerStatus
from utils import convert_time_to_timestamp
from services import transition_menu


async def add_money_data_to_db(
    state_data,  # TODO
    message: types.Message,
    money: Union[float, None]
) -> None:
    """Запись информации о деньгах в бд"""
    action = state_data.get("action")
    add_time = convert_time_to_timestamp(datetime.now())
    record_category = state_data.get("record_category")
    if action == Action.expenses.value:
        await db.add_my_expenses(
            message.from_user.id, record_category, money, add_time
        )
    elif action == Action.income.value:
        await db.add_my_income(
            message.from_user.id, record_category, money, add_time
        )
    elif action == Action.investments.value:
        await db.add_my_investments(
            message.from_user.id, record_category, money, add_time
        )
    else:
        raise NotImplementedError
    await message.answer("Запись сделана успешно")
    await transition_menu.to_filling_menu(message, action)
    await OwnerStatus.in_fill_data_menu.set()
