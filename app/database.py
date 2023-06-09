from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@' \
                          f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
print(SQLALCHEMY_DATABASE_URL)
# 'postgresql://postgres:1324@localhost/blog'

# engine is responsible for establishing connection to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# to talk to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all our models will be extending this base class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
