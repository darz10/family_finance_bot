
from database.db_connect import get_asyncpg_pool


async def get_my_expenses(user_id: int, against: float, to: float):
    """Получить данные о личных тратах"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """
            SELECT expenses.health, expenses.education, expenses.entertainment,
            expenses.travaling, expenses.food,
            expenses.apartment, expenses.internet_and_connection,
            expenses.large_purchases, expenses.extra_spending
            FROM expenses
            INNER JOIN user_expenses ON expenses.id = user_expenses.id
            INNER JOIN users ON user_expenses.user_id = users.id
            WHERE users.user_id = $1
            AND $2 <= expenses.add_time
            AND expenses.add_time <= $3
            """,
            user_id,
            against,
            to,
        )
        return data


async def get_my_income(user_id: int, against: float, to: float):
    """Получить данные о личной прибыли"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """
            SELECT income.salary, income.part_time_job,
            income.dividends_and_coupons
            FROM income
            INNER JOIN user_income ON income.id = user_income.id
            INNER JOIN users ON user_income.user_id = users.id
            WHERE users.user_id = $1
            AND $2 <= income.add_time
            AND income.add_time <= $3
            """,
            user_id,
            against,
            to,
        )
        return data


async def get_my_investments(user_id: int, against: float, to: float):
    """Получить данные о личных инвестициях"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """SELECT investments.invested, investments.total_amount
            FROM investments
            INNER JOIN user_investments ON investments.id = user_investments.id
            INNER JOIN users ON user_investments.user_id = users.id
            WHERE users.user_id = $1
            AND $2 <= investments.add_time
            AND investments.add_time <= $3""",
            user_id,
            against,
            to,
        )
        return data


async def get_family_expenses(against: float, to: float):
    """Получить данные о семейных тратах"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """SELECT SUM(health) AS health,
            SUM(education) AS education,
            SUM(entertainment) AS entertainment,
            SUM(travaling) AS travaling,
            SUM(food) AS food,
            SUM(apartment) AS apartment,
            SUM(internet_and_connection) AS internet_and_connection,
            SUM(large_purchases) AS large_purchases,
            SUM(extra_spending) AS extra_spending
            FROM expenses
            WHERE $1 <= add_time
            AND add_time <= $2
            """,
            against,
            to,
        )
        return data


async def get_family_income(against: float, to: float):
    """Получить данные о семейной прибыли"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """
            SELECT SUM(salary) AS salary,
            SUM(part_time_job) AS part_time_job,
            SUM(dividends_and_coupons) AS dividends_and_coupons
            FROM income
            WHERE $1 <= add_time
            AND add_time <= $2
            """,
            against,
            to,
        )
        return data


async def get_family_investments(against: float, to: float):
    """Получить данные о семейных инвестициях"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """
            SELECT SUM(invested) AS invested,
            SUM(total_amount) AS total_amount
            FROM investments
            WHERE $1 <= add_time
            AND add_time <= $2
            """,
            against,
            to,
        )
        return data


async def add_my_expenses(
    user_id: int, field: str, value: float, add_time: float
):
    """Добавить данные о личных тратах"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        await c.execute(
            f"""
            WITH exp AS (INSERT INTO expenses({field}, user_id, add_time)
            VALUES ($2, (SELECT id FROM users WHERE user_id = $1), $3)
            RETURNING id)
            INSERT INTO user_expenses(id, user_id)
            VALUES ((SELECT id FROM exp),
            (SELECT id FROM users WHERE user_id = $1))
            """,
            user_id,
            value,
            add_time,
        )


async def add_my_income(
    user_id: int, field: str, value: float, add_time: float
):
    """Добавить данные о личных доходах"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        await c.execute(
            """
            WITH inc AS (INSERT INTO income($4, user_id, add_time)
            VALUES ($2, (SELECT id FROM users WHERE user_id = $1), $3)
            RETURNING id)
            INSERT INTO user_income(id, user_id)
            VALUES ((SELECT id FROM inc),
            (SELECT id FROM users WHERE user_id = $1))""",
            user_id,
            value,
            add_time,
            field
        )


async def add_my_investments(
    user_id: int, field: str, value: float, add_time: float
):
    """Добавить данные о личных инвестициях"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        await c.execute(
            """
            WITH invest AS (INSERT INTO investments($4, user_id, add_time)
            VALUES ($2, (SELECT id FROM users WHERE user_id = $1), $3)
            RETURNING id)
            INSERT INTO user_investments(id, user_id)
            VALUES ((SELECT id FROM invest),
            (SELECT id FROM users WHERE user_id = $1))""",
            user_id,
            value,
            add_time,
            field
        )


async def get_total_invest(user_id: int):
    """Получить общую сумму проинвестированного"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        data = await c.fetch(
            """
            SELECT SUM(investments.total_amount) AS total_amount
            FROM investments
            INNER JOIN user_investments ON investments.id = user_investments.id
            INNER JOIN users ON user_investments.user_id = users.id
            WHERE users.user_id = $1
            """,
            user_id,
        )
        return data
