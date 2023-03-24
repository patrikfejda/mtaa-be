from fastapi import APIRouter, Request, Form
from app.model.status import statusCreate, statusGet, statusGetAll, statusDelete
from app.auth.verify import verifyToken

router = APIRouter()


@router.post("/v1/status")
async def routerCreateStatus(
    status: str = Form(...),
    latitude: str = Form(...),
    longitude: str = Form(...),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    status = statusCreate(status, id, latitude, longitude)
    return {
        "detail": "ok",
        "status": status,
    }


@router.get("/v1/status")
async def routerGetStatus(statusId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    status = statusGet(statusId)
    return {
        "detail": "ok",
        "status": status,
    }


@router.get("/v1/status/all")
async def routerGetAllStatus(request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    statuses = statusGetAll()
    return {
        "detail": "ok",
        "statuses": statuses,
    }


@router.delete("/v1/status")
async def routerDeleteStatus(statusId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    statusDelete(id, statusId)
    return {
        "detail": "ok",
    }
