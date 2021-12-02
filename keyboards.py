from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

register_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).row(
    KeyboardButton(
        "Зарегистрироваться 🔐",
        request_contact=True,
    )
)

button_plug = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).row(KeyboardButton("Главное меню 👑"))


main_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Мои финансы 👨🏼‍💻", callback_data="my_finance"),
    InlineKeyboardButton(
        "Финансы семьи 👨‍👩‍👦",
        callback_data="family_finance",
    ),
)

my_finance_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Мои траты", callback_data="my_expenses"),
    InlineKeyboardButton("Мои доходы", callback_data="my_income"),
    InlineKeyboardButton("Мои инвестиции", callback_data="my_investments"),
    InlineKeyboardButton("Назад", callback_data="back"),
)

family_finance_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Наши траты", callback_data="family_expenses"),
    InlineKeyboardButton("Наши доходы", callback_data="family_income"),
    InlineKeyboardButton(
        "Наши инвестиции", callback_data="family_investments"
    ),
    InlineKeyboardButton("Назад", callback_data="back"),
)

menu_choice_action = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        "📈Посмотреть текущую ситуацию", callback_data="view_situation"
    ),
    InlineKeyboardButton("Ввести данные", callback_data="fill_data"),
    InlineKeyboardButton("Назад", callback_data="back"),
)

menu_expenses = InlineKeyboardMarkup(row_width=3).add(
    InlineKeyboardButton("Здоровье", callback_data="record_health"),
    InlineKeyboardButton("Еда", callback_data="record_food"),
    InlineKeyboardButton("Образование", callback_data="record_education"),
    InlineKeyboardButton("Квартира", callback_data="record_apartment"),
    InlineKeyboardButton("Развлечения", callback_data="record_entertainment"),
    InlineKeyboardButton("Путешествия", callback_data="record_travaling"),
    InlineKeyboardButton(
        "Интернет и связь", callback_data="record_internet_and_connection"
    ),
    InlineKeyboardButton(
        "Крупные покупки", callback_data="record_large_purchases"
    ),
    InlineKeyboardButton(
        "Непредвиденные траты", callback_data="record_extra_spending"
    ),
    InlineKeyboardButton("Назад", callback_data="back"),
)


menu_income = InlineKeyboardMarkup(row_width=3).add(
    InlineKeyboardButton("Зарплата", callback_data="record_salary"),
    InlineKeyboardButton("Подработки", callback_data="record_part_time_job"),
    InlineKeyboardButton(
        "Прибыль с дивидендов", callback_data="record_dividends_and_coupons"
    ),
    InlineKeyboardButton("Назад", callback_data="back"),
)


menu_investments = InlineKeyboardMarkup(row_width=3).add(
    InlineKeyboardButton("Проинвестированно", callback_data="record_invested"),
    InlineKeyboardButton("Назад", callback_data="back"),
)

menu_back = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Назад", callback_data="back"),
)
