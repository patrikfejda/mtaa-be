from fastapi import FastAPI

from app.router import router

app = FastAPI(title="mtaa")
app.include_router(router)
