from aiogram import types

import database.query as db
import keyboards
from utils import get_inteval_time
from constants import Action, TypeFinance


async def to_record(callback_query: types.CallbackQuery) -> None:
    """Переход к вводу данных"""
    bot = callback_query.bot
    text = """Введите сумму числом в формате "123.12" или "451"(без ковычек),"
           " для выхода из ввода данных введите /start"""
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
    )


async def to_menu_category_data(
    callback_query: types.CallbackQuery,
    state_data
) -> None:
    """Переход к меню с отображением данных по категории"""
    bot = callback_query.bot
    text = ""
    against, to = get_inteval_time()
    if state_data.get("action") == Action.expenses.value:
        if state_data.get("type") == TypeFinance.my_finance.value:
            expenses_data = await db.get_my_expenses(
                callback_query.from_user.id, against, to
            )
        elif state_data.get("type") == TypeFinance.family_finance.value:
            expenses_data = await db.get_family_expenses(against, to)
        health = 0
        food = 0
        education = 0
        apartment = 0
        entertainment = 0
        travaling = 0
        internet_and_connection = 0
        large_purchases = 0
        extra_spending = 0
        for item in expenses_data:
            if item.get("health"):
                health += item.get("health")
            if item.get("food"):
                food += item.get("food")
            if item.get("education"):
                education += item.get("education")
            if item.get("apartment"):
                apartment += item.get("apartment")
            if item.get("entertainment"):
                entertainment += item.get("entertainment")
            if item.get("travaling"):
                travaling += item.get("travaling")
            if item.get("internet_and_connection"):
                internet_and_connection += item.get("internet_and_connection")
            if item.get("large_purchases"):
                large_purchases += item.get("large_purchases")
            if item.get("extra_spending"):
                extra_spending += item.get("extra_spending")
        text += f"Здоровье: {health}\nЕда: {food}\nОбразование: {education}\n"\
                f"Квартира: {apartment}\nРазвлечения: {entertainment}\n"\
                f"Путешествия: {travaling}\n"\
                f"Связь и интернет: {internet_and_connection}\n"\
                f"Крупные траты: {large_purchases}\n"\
                f"Непредвиденные траты: {extra_spending}\n"

    elif state_data.get("action") == Action.income.value:
        if state_data.get("type") == TypeFinance.my_finance.value:
            income_data = await db.get_my_income(
                callback_query.from_user.id, against, to
            )
        elif state_data.get("type") == TypeFinance.family_finance.value:
            income_data = await db.get_family_income(against, to)
        salary = 0
        part_time_job = 0
        dividends_and_coupons = 0
        for item in income_data:
            if item.get("salary"):
                salary += item.get("salary")
            if item.get("part_time_job"):
                part_time_job += item.get("part_time_job")
            if item.get("dividends_and_coupons"):
                dividends_and_coupons += item.get("dividends_and_coupons")
        text = f"Зарплата: {salary}\nПодработки: {part_time_job}\n"\
               f"Прибыль с дивидендов: {dividends_and_coupons}"
    elif state_data.get("action") == Action.investments.value:
        if state_data.get("type") == TypeFinance.my_finance.value:
            investments_data = await db.get_my_investments(
                callback_query.from_user.id, against, to
            )
            total = await db.get_total_invest(callback_query.from_user.id)
        elif state_data.get("type") == TypeFinance.family_finance.value:
            investments_data = await db.get_my_investments(against, to)
        invested = 0
        total_amount = 0
        if total:
            total_amount += total
        for item in investments_data:
            if item.get("invested"):
                invested += item.get("invested")
        text = f"Проинвестированно: {invested}\n"\
               f"Общая сумма инветиций: {total_amount}\n"
    else:
        raise NotImplementedError
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboards.menu_back,
    )


async def to_menu_choice_action(callback_query: types.CallbackQuery) -> None:
    """Переход к меню выбора действия"""
    bot = callback_query.bot
    keyboard = keyboards.menu_choice_action
    text = "Выбери действие"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_my_finance_menu(callback_query: types.CallbackQuery) -> None:
    """Переход к меню личных финансов"""
    bot = callback_query.bot
    keyboard = keyboards.my_finance_menu
    text = "Мои финансы"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_main_menu(callback_query: types.CallbackQuery) -> None:
    """Переход к главному меню"""
    bot = callback_query.bot
    keyboard = keyboards.main_menu
    text = "Главное меню"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_family_finance_menu(
    callback_query: types.CallbackQuery
) -> None:
    """Переход к меню семейных финансов"""
    keyboard = keyboards.family_finance_menu
    text = "Финансы семьи"
    bot = callback_query.bot
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_filling_menu(
    callback_query: types.CallbackQuery,
    action
) -> None:
    text = "Выберите категорию для ввода данных"
    keyboard = None
    bot = callback_query.bot
    try:
        if action == Action.expenses.value:
            keyboard = keyboards.menu_expenses
        if action == Action.income.value:
            keyboard = keyboards.menu_income
        if action == Action.investments.value:
            keyboard = keyboards.menu_investments
        await bot.edit_message_text(
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=keyboard,
            )
    except AttributeError:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=text,
            reply_markup=keyboard,
        )
