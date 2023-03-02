from fastapi import APIRouter

from app.database import cur
 
router = APIRouter()

@router.get("/v1/dbhealth")
async def healthcheck():
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    return {"version": version}
