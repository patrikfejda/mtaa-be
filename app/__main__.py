from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import router
from app.config import FILESTORE_PATH, FILESTORE_URL, settings
from app.db.init_db import init_db
from app.db.orm import SessionLocal

app = FastAPI(title="mtaa")
app.include_router(router, prefix=settings.API_PREFIX)
app.mount(FILESTORE_URL, StaticFiles(directory=FILESTORE_PATH), name="static")


def main():
    print("Initializing database")
    db = SessionLocal()
    init_db(db)
    print("Database initialized")


main()
