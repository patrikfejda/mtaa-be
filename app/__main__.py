from fastapi import FastAPI
from app.model.classes import createTables
from fastapi.staticfiles import StaticFiles
from app.config import FILESTORE_PATH, FILESTORE_URL

from app.router import router

app = FastAPI(title="mtaa")
app.include_router(router)
app.mount(FILESTORE_URL, StaticFiles(directory=FILESTORE_PATH), name="static")

createTables()
