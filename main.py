import asyncio
from datetime import datetime
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.redis import RedisStorage
from settings import settings
from status import OwnerStatus
from keyboards import (
    register_keyboard,
    main_menu,
    my_finance_menu,
    family_finance_menu,
    menu_choice_action,
    menu_expenses,
    menu_income,
    menu_investments,
    menu_back,
    button_plug,
)
from validation import valid_phone_number, valid_money
import db
from constants import Action, TypeFinance

token = settings.token_bot

bot = Bot(token=token)

storage = RedisStorage(
    host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
)

dp = Dispatcher(bot, storage=storage)

logging.basicConfig(filename="logs.log", level=logging.INFO)
logger = logging.getLogger("logs")


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    try:

        status = await state.get_state()
        if status is not None:
            if status == OwnerStatus.unregistred.state:
                await message.answer(
                    "Зарегайся плиз ;)", reply_markup=register_keyboard
                )
                await OwnerStatus.unregistred.set()
            elif status == OwnerStatus.no_access.state:
                await message.answer(
                    "К сожалению ты пока не можешь пользоваться приложением :(, обратись к ```{}```".format(
                        settings.dev_link
                    )
                )
                await OwnerStatus.no_access.set()
            else:
                await message.answer("Воспользуйся приложением ;)")
                await OwnerStatus.in_main_menu.set()
        else:
            await message.answer(
                "Зарегайся плиз ;)", reply_markup=register_keyboard
            )
            await OwnerStatus.unregistred.set()
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при выполнении команды /start\n{}".format(
                e
            ),
        )


@dp.message_handler(state="*")
async def others_messages(message: types.Message, state: FSMContext):
    """Обработчик сообщений"""
    try:
        status = await state.get_state()
        state_data = await state.get_data()
        if status is not None:
            if status == OwnerStatus.unregistred.state:
                await message.answer(
                    "Для начала зарегистрируйся, а потом поговорим",
                    reply_markup=register_keyboard,
                )
            elif status == OwnerStatus.no_access.state:
                await message.answer(
                    "К сожалению тебе сюда доступ запрещён, обратись к  ```{}```".format(
                        settings.dev_link
                    )
                )
                await OwnerStatus.no_access.set()
            elif status == OwnerStatus.in_record_data_menu.state:
                message_data = message.text
                money = valid_money(message_data)
                if money:
                    await handler_money_data(state_data, message, money)
                else:
                    await message.answer(
                        "Введен неверный денежный формат, повторите попытку"
                    )
            else:
                await message.answer(
                    "Ты уже можешь использовать все функции",
                    reply_markup=main_menu,
                )
                await OwnerStatus.in_main_menu.set()
        else:
            await message.answer(
                "Для начала зарегистрируйся",
                reply_markup=register_keyboard,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при отправке сообщения\n{}".format(
                e
            ),
        )


async def handler_money_data(state_data, message, money):
    """Запись информации о деньгах в бд"""
    action = state_data.get("action")
    date_now = datetime.now()
    add_time = date_now.timestamp() * 1e6
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
    await to_fill_data_menu(message, action)
    await OwnerStatus.in_fill_data_menu.set()


@dp.message_handler(
    state=[OwnerStatus.unregistred], content_types=types.ContentType.CONTACT
)
async def registred(message: types.Message, state: FSMContext):
    """Регистрация пользователя"""
    try:
        if message.contact.user_id != message.from_user.id:
            await message.answer(
                "Вы отправили не свой номер телефона, пожалуйста введите снова",
                reply_markup=register_keyboard,
            )
        else:
            check_number = valid_phone_number(
                str(message.contact.phone_number)
            )
            if check_number is None:
                await message.answer(
                    "Формат номера телефона неверный, пожалуйста повторите"
                )
            else:
                if int(check_number) in settings.access_phone_numbers:
                    first_name = message.from_user.first_name
                    last_name = message.from_user.last_name
                    user_id = message.from_user.id
                    phone_number = check_number
                    await db.create_user(
                        first_name, last_name, user_id, phone_number
                    )
                    await message.answer(
                        "Регистрация прошла успешно", reply_markup=button_plug
                    )
                else:
                    await message.answer(
                        "К сожалению ты пока не можешь пользоваться приложением  :(, обратись к ..."
                    )
                    await OwnerStatus.no_access.set()
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при регистрации\n{}".format(e),
        )


@dp.callback_query_handler(
    lambda c: c.data in ["my_finance"],
    state=[
        OwnerStatus.in_main_menu,
        OwnerStatus.in_menu_choice_action,
    ],
)
async def my_finance(callback_query: types.CallbackQuery, state: FSMContext):
    """Меню моих финансов"""
    try:
        state = dp.get_current().current_state()
        await state.update_data(type=TypeFinance.my_finance.value)
        await to_my_finance_menu(callback_query)
        await OwnerStatus.in_my_finance_menu.set()
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot в меню личных финансов\n{}".format(
                e
            ),
        )


@dp.callback_query_handler(
    lambda c: c.data in ["family_finance"],
    state=[
        OwnerStatus.in_main_menu,
        OwnerStatus.in_menu_choice_action,
    ],
)
async def family_finance(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Меню семейных финансов"""
    try:
        state = dp.get_current().current_state()
        await state.update_data(type=TypeFinance.family_finance.value)
        await to_family_finance_menu(callback_query)
        await OwnerStatus.in_family_finance_menu.set()
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot в меню семейных финансов\n{}".format(
                e
            ),
        )


@dp.callback_query_handler(
    lambda c: "expenses" in c.data
    or "income" in c.data
    or "investments" in c.data,
    state=[
        OwnerStatus.in_my_finance_menu,
        OwnerStatus.in_family_finance_menu,
    ],
)
async def get_menu_choice_action(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Меню выбора действия"""
    try:
        state = dp.get_current().current_state()
        if "expenses" in callback_query.data:
            await state.update_data(action=Action.expenses.value)
        elif "income" in callback_query.data:
            await state.update_data(action=Action.income.value)
        elif "investments" in callback_query.data:
            await state.update_data(action=Action.investments.value)
        await to_menu_choice_action(callback_query)
        await OwnerStatus.in_menu_choice_action.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot в меню выбора действия\n{}".format(
                e
            ),
        )


@dp.callback_query_handler(
    lambda c: c.data in ["view_situation"],
    state=[
        OwnerStatus.in_menu_choice_action,
    ],
)
async def get_view_situation(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Посмотреть данные по отдельной категории"""
    try:
        state_data = await state.get_data()
        await to_menu_category_data(callback_query, state_data)
        await OwnerStatus.in_view_situation_menu.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при просмотре данных по отдельной категории\n{}".format(
                e
            ),
        )


@dp.callback_query_handler(
    lambda c: c.data in ["fill_data"],
    state=[
        OwnerStatus.in_menu_choice_action,
    ],
)
async def filling_data(callback_query: types.CallbackQuery, state: FSMContext):
    """Выбрать категорию для заполнения"""
    try:
        state_data = await state.get_data()
        state = dp.get_current().current_state()
        action = state_data.get("action")
        await to_fill_data_menu(callback_query, action)
        await OwnerStatus.in_fill_data_menu.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при выборе категории для воода данных\n{}".format(
                e
            ),
        )


@dp.callback_query_handler(
    lambda c: "record_" in c.data,
    state=[OwnerStatus.in_fill_data_menu],
)
async def record_data(callback_query: types.CallbackQuery, state: FSMContext):
    """Записать данные по отдельной категории"""
    try:
        state = dp.get_current().current_state()
        category = callback_query.data[7:]
        await state.update_data(record_category=category)
        await to_record(callback_query)
        await OwnerStatus.in_record_data_menu.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при записи данных\n{}".format(
                e
            ),
        )


async def to_main_menu(callback_query):
    """Переход к главному меню"""
    keyboard = main_menu
    text = "Главное меню"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_my_finance_menu(callback_query):
    """Переход к меню личных финансов"""
    keyboard = my_finance_menu
    text = "Мои финансы"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_family_finance_menu(callback_query):
    """Переход к меню семейных финансов"""
    keyboard = family_finance_menu
    text = "Финансы семьи"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def to_menu_choice_action(callback_query):
    """Переход к меню выбора действия"""
    keyboard = menu_choice_action
    text = "Выбери действие"
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


async def get_inteval_time():
    """Получение timestamp начала месяца и текущей даты"""
    date_now = datetime.now()
    year_now = date_now.year
    month_now = date_now.month
    against_date = datetime(day=1, month=month_now, year=year_now)
    agaist_timestamp = against_date.timestamp() * 1e6
    to_timestamp = date_now.timestamp() * 1e6
    return agaist_timestamp, to_timestamp


async def to_menu_category_data(callback_query, state_data):
    """Переход к меню с отображением данных по категории"""
    text = ""
    against, to = await get_inteval_time()
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
        text += f"Здоровье: {health}\nЕда: {food}\nОбразование: {education}\nКвартира: {apartment}\nРазвлечения: {entertainment}\nПутешествия: {travaling}\nСвязь и интернет: {internet_and_connection}\nКрупные траты: {large_purchases}\nНепредвиденные траты: {extra_spending}\n"

    elif state_data.get("action") == Action.income.value:
        if state_data.get("type") == TypeFinance.my_finance.value:
            income_data = await db.get_my_income(
                callback_query.from_user.id, against, to
            )
        elif state_data.get("type") == TypeFinance.family_finance.value:
            income_data = await db.get_familyy_income(against, to)
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
        text = f"Зарплата: {salary}\nПодработки: {part_time_job}\nПрибыль с дивидендов: {dividends_and_coupons}"
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
        text = f"Проинвестированно: {invested}\nОбщая сумма инветиций: {total_amount}\n"
    else:
        raise NotImplementedError
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
        reply_markup=menu_back,
    )


async def to_fill_data_menu(callback_query, action):
    """Переход к выбору категории ввода данных"""
    text = "Выберите категорию для ввода данных"
    if action == Action.expenses.value:
        keyboard = menu_expenses
    if action == Action.income.value:
        keyboard = menu_income
    if action == Action.investments.value:
        keyboard = menu_investments
    try:
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


async def to_record(callback_query):
    """Переход к вводу данных"""
    text = """Введите сумму числом в формате "123.12" или "451"(без ковычек), для выхода из ввода данных введите /start"""
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=text,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["back"],
    state="*",
)
async def to_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик возврата меню"""
    try:
        status = await state.get_state()
        state_data = await state.get_data()
        if (
            status == OwnerStatus.in_my_finance_menu.state
            or status == OwnerStatus.in_family_finance_menu.state
        ):
            await to_main_menu(callback_query)
            await OwnerStatus.in_main_menu.set()
        elif status == OwnerStatus.in_menu_choice_action.state:
            if state_data.get("type") == TypeFinance.my_finance.value:
                await to_my_finance_menu(callback_query)
                await OwnerStatus.in_my_finance_menu.set()
            elif state_data.get("type") == TypeFinance.family_finance.value:
                await to_family_finance_menu(callback_query)
                await OwnerStatus.in_family_finance_menu.set()
        elif (
            status == OwnerStatus.in_view_situation_menu.state
            or status == OwnerStatus.in_fill_data_menu.state
        ):
            await to_menu_choice_action(callback_query)
            await OwnerStatus.in_menu_choice_action.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при возврате back\n{}".format(
                e
            ),
        )


if __name__ == "__main__":
    asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
