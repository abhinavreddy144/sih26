# SIH26034 Dev

This workspace contains a starter configuration for a PostgreSQL-backed SQLAlchemy and Alembic project.

## Files

- `requirements.txt` for Python dependencies.
- `.env` for the PostgreSQL connection string.
- `app.py` for the SQLAlchemy database engine and session factory.
- `models.py` for the example model.
- `alembic.ini` and `alembic/` directory for Alembic migrations.
- `setup.py` for packaging the project.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## PostgreSQL connection

Set the connection string in `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/sih26034_dev
```

## Alembic

```bash
alembic init alembic
alembic revision -m "create_user_table"
alembic upgrade head
```
