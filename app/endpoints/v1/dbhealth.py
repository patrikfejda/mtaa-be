from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import cur, conn

router = APIRouter()


@router.get("/v1/dbhealth")
async def healthcheck():
    # cur.execute("SELECT version();")
    # version = cur.fetchone()[0]
    result = conn.execute(text("SELECT version();"))
    version = result.one()[0]
    return {"version": version}
