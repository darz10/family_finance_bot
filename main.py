import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.redis import RedisStorage

import services
from settings import settings
from status import OwnerStatus


token = settings.token_bot

bot = Bot(token=token)

storage = RedisStorage(
    host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
)

dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    try:
        await services.start_handler(message, state)
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot"
                 f" при выполнении команды /start\n{e}"
        )


@dp.message_handler(state="*")
async def others_messages(message: types.Message, state: FSMContext):
    """Обработчик сообщений"""
    await services.other_message_handler(message, state)


@dp.message_handler(
    state=[OwnerStatus.unregistred], content_types=types.ContentType.CONTACT
)
async def registred(message: types.Message, state: FSMContext):
    """Регистрация пользователя"""
    await services.register_user(message, state)


@dp.callback_query_handler(
    lambda c: c.data in ["my_finance"],
    state=[
        OwnerStatus.in_main_menu,
        OwnerStatus.in_menu_choice_action,
    ],
)
async def my_finance(callback_query: types.CallbackQuery, state: FSMContext):
    """Меню моих финансов"""
    state = dp.get_current().current_state()
    await services.get_my_finance_menu(callback_query, state)


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
    state = dp.get_current().current_state()
    await services.get_family_finance_menu(state, callback_query)


@dp.callback_query_handler(
    lambda c: "expenses" in c.data
    or "income" in c.data
    or "investments" in c.data,
    state=[
        OwnerStatus.in_my_finance_menu,
        OwnerStatus.in_family_finance_menu,
    ],
)
async def menu_choice_action(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Меню выбора действия"""
    state = dp.get_current().current_state()
    await services.get_menu_choice_actions(
        state,
        callback_query
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
    await services.get_view_category(callback_query, state)


@dp.callback_query_handler(
    lambda c: c.data in ["fill_data"],
    state=[
        OwnerStatus.in_menu_choice_action,
    ],
)
async def filling_data(callback_query: types.CallbackQuery, state: FSMContext):
    """Выбрать категорию для заполнения"""
    await services.get_fill_data_menu(callback_query, state)


@dp.callback_query_handler(
    lambda c: "record_" in c.data,
    state=[OwnerStatus.in_fill_data_menu],
)
async def record_data(callback_query: types.CallbackQuery, state: FSMContext):
    """Записать данные по отдельной категории"""
    state = dp.get_current().current_state()
    await services.get_record_data_menu(callback_query, state)


@dp.callback_query_handler(
    lambda c: c.data in ["back"],
    state="*",
)
async def to_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик возврата меню"""
    await services.get_back_menu(callback_query, state)


if __name__ == "__main__":
    asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
