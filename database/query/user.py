
from constants import Role
from database.db_connect import get_asyncpg_pool


async def create_user(
    first_name: str, last_name: str, user_id: int, phone_number: str
):
    """Добавление пользователя в бд"""
    db = await get_asyncpg_pool()
    async with db.acquire() as c:
        await c.execute(
            """
            WITH t AS(INSERT INTO users(
                first_name, last_name,
                user_id, phone_number
            )
            VALUES ($1, $2, $3, $4) RETURNING id)
            INSERT INTO users_to_roles(role_id, user_id)
            VALUES ($5, (SELECT id FROM t))
            """,
            first_name,
            last_name,
            user_id,
            phone_number,
            Role.USER.value,
        )
