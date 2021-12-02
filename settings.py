from typing import List
from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    """Валидация данных конфигруации"""

    token_bot: str = Field(..., description="Токен бота")

    pg_connection: PostgresDsn = Field(
        ..., description="Подключение к postgresql"
    )
    redis_host: str = Field(..., description="Хост для подключения redis")
    redis_port: int = Field(..., description="Порт для подключения redis")
    redis_db: int = Field(..., description="Бд для подключения redis")

    dev_id: int = Field(
        ..., description="Id разработчика для получения сообщений об ошибках"
    )
    dev_link: int = Field(..., description="Ссылка на профиль разработчика")

    access_phone_numbers: List[int] = Field(
        ...,
        description="Список номеров имеющих доступ к пользованию приложением",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "tg_"


settings = Settings()
