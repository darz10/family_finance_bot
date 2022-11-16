from setuptools import setup, find_packages

setup(
    name="Finance_family_bot",
    version="0.1.0",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pydantic==1.8.2",
        "aiogram==2.14.3",
        "asyncpg==0.24.0",
        "aioredis==1.3.1",
        "python-dotenv==0.20.0"

    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-pylint",
            "pytest-asyncio",
            "pytest-postgresql",
            "psycopg2-binary",
        ]
    },
    author="Vedernikov Artem",
    author_email="vedernikov.tema1996@gmail.com",
)
