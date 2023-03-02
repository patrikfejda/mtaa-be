import psycopg2
from app.config import settings


cur = psycopg2.connect(
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    user=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,
    database=settings.DATABASE_NAME,
).cursor()
