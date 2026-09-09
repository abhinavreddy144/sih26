# SIH26034 Dev

This workspace contains a PostgreSQL-backed SQLAlchemy and Alembic project for SIH26 inspection and compliance evidence processing.

## Project files

- `requirements.txt` for Python dependencies.
- `.env` for the PostgreSQL connection string.
- `app.py` for the application entry point.
- `database.py` for the SQLAlchemy engine and session factory.
- `models.py` for the ORM entities.
- `repositories.py` for repository operations.
- `alembic.ini` and `alembic/` for Alembic migration configuration.
- `migrations/versions/` for migration revisions.
- `storage/images` and `storage/reports` for evidence and report artifacts.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## PostgreSQL connection

Set the PostgreSQL DSN in `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/sih26034_dev
```

## Alembic

```bash
alembic upgrade head
```

## Repository status

This repository stores the inspection database and related repository-backed project artifacts.
