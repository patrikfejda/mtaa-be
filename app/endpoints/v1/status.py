from fastapi import APIRouter, Header, Request, Form, File, UploadFile
from typing import Annotated, List, Union, Optional
from typing import Union
from pydantic import BaseModel
from app.model.status import statusCreate, statusGet, statusGetAll, statusDelete
from app.auth.verify import verify_token
from app.filestore.save import save_upload_file

router = APIRouter()


@router.post("/v1/status")
async def createStatus(
    status: str = Form(...),
    latitude: str = Form(...),
    longitude: str = Form(...),
    request: Request = None
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    status = statusCreate(status, id, latitude, longitude)
    return {
        "detail": "ok",
        "status": status,
    }
