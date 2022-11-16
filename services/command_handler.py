from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from services.service_db import add_money_data_to_db

from status import OwnerStatus
from settings import settings
import keyboards
from utils import convert_money_to_float


async def start_handler(message: types.Message, state: FSMContext):
    status = await state.get_state()
    if not status:
        if status == OwnerStatus.unregistred.state:
            await message.answer(
                "Зарегайся плиз ;)",
                reply_markup=keyboards.register_keyboard
            )
            await OwnerStatus.unregistred.set()
        elif status == OwnerStatus.no_access.state:
            await message.answer(
                "К сожалению ты пока не можешь пользоваться приложением"
                f" :(, обратись к ```{settings.dev_link}```"
            )
            await OwnerStatus.no_access.set()
        else:
            await message.answer("Воспользуйся приложением ;)")
            await OwnerStatus.in_main_menu.set()
    else:
        await message.answer(
            "Зарегайся плиз ;)",
            reply_markup=keyboards.register_keyboard
        )
        await OwnerStatus.unregistred.set()


async def other_message_handler(
    message: types.Message,
    state: FSMContext
) -> None:
    """
    Обработчик сообщений не входящих в команды бота
    """
    bot = message.bot
    try:
        status = await state.get_state()
        state_data = await state.get_data()
        if not status:
            if status == OwnerStatus.unregistred.state:
                await message.answer(
                    "Для начала зарегистрируйся, а потом поговорим",
                    reply_markup=keyboards.register_keyboard,
                )
            elif status == OwnerStatus.no_access.state:
                await message.answer(
                    "К сожалению тебе сюда доступ запрещён,"
                    f" обратись к  ```{settings.dev_link}```"
                )
                await OwnerStatus.no_access.set()
            elif status == OwnerStatus.in_record_data_menu.state:
                message_data = message.text
                money = convert_money_to_float(message_data)
                if money:
                    await add_money_data_to_db(state_data, message, money)
                else:
                    await message.answer(
                        "Введен неверный денежный формат, повторите попытку"
                    )
            else:
                await message.answer(
                    "Ты уже можешь использовать все функции",
                    reply_markup=keyboards.main_menu,
                )
                await OwnerStatus.in_main_menu.set()
        else:
            await message.answer(
                "Для начала зарегистрируйся",
                reply_markup=keyboards.register_keyboard,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=settings.dev_id,
            text=f"Произошла ошибка в Financebot при отправке сообщения\n{e}"
        )
