from setuptools import setup, find_packages

setup(
    name="sih26034-dev",
    version="0.1.0",
    description="SQLAlchemy + Alembic + PostgreSQL starter",
    packages=find_packages(),
    install_requires=[
        "SQLAlchemy==2.0.36",
        "alembic==1.14.0",
        "psycopg2-binary==2.9.10",
        "python-dotenv==1.0.1",
    ],
)
