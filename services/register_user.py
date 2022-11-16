from aiogram import types
from aiogram.dispatcher.storage import FSMContext

import database.query as db
import keyboards
from settings import settings
from status import OwnerStatus
from utils import clear_phone
from services.menu_actions import logger


async def register_user(message: types.Message, state: FSMContext):
    """
    Метод регитрации пользователя
    """
    bot = message.bot
    try:
        if message.contact.user_id != message.from_user.id:
            await message.answer(
                "Вы отправили не свой номер телефона,"
                " пожалуйста введите снова",
                reply_markup=keyboards.register_keyboard,
            )
        else:
            check_number = clear_phone(
                str(message.contact.phone_number)
            )
            if not check_number:
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
                    await OwnerStatus.in_main_menu.set()
                    await message.answer(
                        "Регистрация прошла успешно",
                        reply_markup=keyboards.button_plug
                    )
                else:
                    await message.answer(
                        "К сожалению ты пока не можешь пользоваться"
                        " приложением  :(, обратись к ..."
                    )
                    await OwnerStatus.no_access.set()
    except Exception as e:
        logger.exception(f"{e}")
        await bot.send_message(
            chat_id=settings.dev_id,
            text="Произошла ошибка в Financebot при"
                 f" выборе категории для воода данных\n{e}"
        )
