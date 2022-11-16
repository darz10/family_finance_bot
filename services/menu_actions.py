import logging

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from settings import settings
from constants import Action, TypeFinance
from status import OwnerStatus
from services import transition_menu


logging.basicConfig(filename="logs.log", level=logging.INFO)
logger = logging.getLogger("logs")


async def get_my_finance_menu(
    callback_query: types.CallbackQuery,
    state: FSMContext
) -> None:
    bot = callback_query.bot
    try:
        await state.update_data(type=TypeFinance.my_finance.value)
        await transition_menu.to_my_finance_menu(callback_query)
        await OwnerStatus.in_my_finance_menu.set()
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text=f"Произошла ошибка в Financebot в меню личных финансов\n{e}"
        )


async def get_view_category(callback_query, state):  # TODO
    bot = callback_query.bot
    try:
        state_data = await state.get_data()
        await transition_menu.to_menu_category_data(callback_query, state_data)
        await OwnerStatus.in_view_situation_menu.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при просмотре данных"
                 f" по отдельной категории\n{e}"
        )


async def get_fill_data_menu(
    callback_query: types.CallbackQuery,
    state
):  # TODO annotations
    """Переход к выбору категории ввода данных"""
    bot = callback_query.bot
    try:
        state_data = await state.get_data()
        action = state_data.get("action")
        await transition_menu.to_filling_menu(callback_query, action)
        await OwnerStatus.in_fill_data_menu.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при выборе"
                 f" категории для воода данных\n{e}"
        )


async def get_back_menu(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    bot = callback_query.bot
    try:
        status = await state.get_state()
        state_data = await state.get_data()
        if (
            status == OwnerStatus.in_my_finance_menu.state
            or status == OwnerStatus.in_family_finance_menu.state
        ):
            await transition_menu.to_main_menu(callback_query)
            await OwnerStatus.in_main_menu.set()
        elif status == OwnerStatus.in_menu_choice_action.state:
            if state_data.get("type") == TypeFinance.my_finance.value:
                await transition_menu.to_my_finance_menu(callback_query)
                await OwnerStatus.in_my_finance_menu.set()
            elif state_data.get("type") == TypeFinance.family_finance.value:
                await transition_menu.to_family_finance_menu(callback_query)
                await OwnerStatus.in_family_finance_menu.set()
        elif (
            status == OwnerStatus.in_view_situation_menu.state
            or status == OwnerStatus.in_fill_data_menu.state
        ):
            await transition_menu.to_menu_choice_action(callback_query)
            await OwnerStatus.in_menu_choice_action.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при возврате back\n{}".format(
                e
            ),
        )


async def get_menu_choice_actions(state, callback_query):  # TODO
    bot = callback_query.bot
    try:
        if "expenses" in callback_query.data:
            await state.update_data(action=Action.expenses.value)
        elif "income" in callback_query.data:
            await state.update_data(action=Action.income.value)
        elif "investments" in callback_query.data:
            await state.update_data(action=Action.investments.value)
        await transition_menu.to_menu_choice_action(callback_query)
        await OwnerStatus.in_menu_choice_action.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text=f"Произошла ошибка в Financebot в меню выбора действия\n{e}"
        )


async def get_family_finance_menu(state, callback_query):  # TODO
    bot = callback_query.bot
    try:
        await state.update_data(type=TypeFinance.family_finance.value)
        await transition_menu.to_family_finance_menu(callback_query)
        await OwnerStatus.in_family_finance_menu.set()
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text=f"Произошла ошибка в Financebot в меню семейных финансов\n{e}"
        )


async def get_record_data_menu(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    bot = callback_query.bot
    try:
        category = callback_query.data[7:]  # TODO исправить интексы
        await state.update_data(record_category=category)
        await transition_menu.to_record(callback_query)
        await OwnerStatus.in_record_data_menu.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text=f"Произошла ошибка в Financebot при записи данных\n{e}"
        )
