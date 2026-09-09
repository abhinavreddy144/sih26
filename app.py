import os
from dotenv import load_dotenv
from database import Base, engine, init_db, SessionLocal

load_dotenv()

if __name__ == '__main__':
    try:
        init_db()
        print('SQLAlchemy PostgreSQL connection successful.')
    except Exception as exc:
        print(f'PostgreSQL connection failed: {exc}')
