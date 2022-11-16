from datetime import datetime
from typing import Tuple, Union


def convert_time_to_timestamp(time: datetime) -> datetime:
    """
    Конвертация объектов типа datetime
    в формат timestamp
    """
    return time.timestamp() * 1e6


def get_inteval_time() -> Tuple[datetime, datetime]:
    """
    Получение timestamp начала месяца и текущей даты
    """
    date_now = datetime.now()
    year_now = date_now.year
    month_now = date_now.month
    against_date = datetime(day=1, month=month_now, year=year_now)
    agaist_timestamp = convert_time_to_timestamp(against_date)
    to_timestamp = convert_time_to_timestamp(date_now)
    return agaist_timestamp, to_timestamp


def convert_money_to_float(money: str) -> Union[float, None]:
    """Конвератацияправильности ввода денег"""
    try:
        num_money = float(money)
        if num_money:
            return float(money)
    except ValueError:
        return None


def clear_phone(phone: str) -> str:
    '''
    Очищаем телефон от посторонних символов.
    '''
    clear_phone = filter(str.isdigit, phone)
    return ''.join(clear_phone)
