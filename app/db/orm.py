from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

host = settings.DATABASE_HOST
port = settings.DATABASE_PORT
user = settings.DATABASE_USER
password = settings.DATABASE_PASSWORD
database = settings.DATABASE_NAME


engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
