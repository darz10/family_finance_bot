def valid_phone_number(phone_number: str):
    """Проверка номера телефона"""
    if phone_number.startswith("+79") and len(phone_number) == 12:
        phone_number = phone_number[1:]
        return phone_number
    elif phone_number.startswith("79") and len(phone_number) == 11:
        return phone_number


def valid_money(money: str):
    """Проверка правильности ввода денег"""
    try:
        num_money = float(money)
        if num_money:
            return float(money)
    except ValueError:
        return None