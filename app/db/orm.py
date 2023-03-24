from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql://postgres:postgres@mtaa-db:5432/mtaa_db", future=True
)

Session = sessionmaker(bind=engine)
session = Session()
