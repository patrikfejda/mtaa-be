from fastapi import APIRouter

router = APIRouter()


@router.get("/v1/health")
async def routerHealthcheck():
    return {"status": 200, "message": "Alive as never before."}
