from enum import Enum


class Role(Enum):
    ADMIN = 1
    USER = 2


class TypeFinance(Enum):
    family_finance = "family_finance"
    my_finance = "my_finance"


class Action(Enum):
    expenses = "expenses"
    income = "income"
    investments = "investments"
