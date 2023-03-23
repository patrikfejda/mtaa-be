from fastapi import FastAPI
from app.model.classes import create_tables

from app.router import router

app = FastAPI(title="mtaa")
app.include_router(router)

create_tables()
