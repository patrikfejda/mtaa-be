import psycopg2
from app.config import settings
from sqlalchemy import create_engine

host = settings.DATABASE_HOST
port = settings.DATABASE_PORT
user = settings.DATABASE_USER
password = settings.DATABASE_PASSWORD
database = settings.DATABASE_NAME

cur = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
).cursor()

engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{database}", future=True
)

conn = engine.connect()


# def connect(db_uri):
#     engine = create_engine(db_uri)
#     return engine.connect()


# database = settings.DATABASE_NAME

# try:
#     db_uri = os.path.expandvars(
#         f"postgresql://{user}:{password}@{host}:{port}/{database}"
#     )
#     db_uri = urllib.parse.unquote(db_uri)
#     conn = connect(db_uri)
# except Exception as e:
#     print("Failed to connect to database.")
#     print("{0}".format(e))
