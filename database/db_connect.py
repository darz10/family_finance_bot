import ssl
from asyncpg import create_pool

from settings import settings


pool = None


async def get_asyncpg_pool():
    global pool
    if pool is None:
        ctx = ssl.create_default_context(cafile="")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        pool = await create_pool(settings.pg_connection, ssl=ctx)
    return pool
