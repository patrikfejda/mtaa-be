from fastapi import APIRouter, Header, Request, Form, File, UploadFile
from typing import Annotated, List, Union, Optional
from typing import Union
from pydantic import BaseModel
from app.model.user import userCreate, userLogin, userGet, userUpdate, userGetAll
from app.auth.verify import verify_token
from app.handlefilestore.save import save_upload_file

router = APIRouter()


@router.post("/v1/user/register")
async def registerUser(
    email: str = Form(...), username: str = Form(...), password: str = Form(...)
):
    jwt, createdUser = userCreate(email=email, username=username, password=password)
    return {"access_token": jwt, "user": createdUser}


@router.post("/v1/user/login")
async def loginUser(username: str = Form(...), password: str = Form(...)):
    jwt, user = userLogin(username=username, password=password)
    return {"access_token": jwt, "user": user}


@router.get("/v1/user")
async def getUser(id: str = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    user = userGet(
        id=id,
    )
    return {"user1": user}


@router.put("/v1/user")
async def updateUser(
    display_name: str = Form(None),
    profile_photo: UploadFile = File(None),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    uploaded_photo_url = save_upload_file(profile_photo)
    user = userUpdate(id, display_name, uploaded_photo_url)
    return {
        "detail": user['id'],
        "display_name": user['display_name'],
        "profile_photo_url": user['profile_photo_url']
    }


@router.get("/v1/user/all")
def getAllUsers():
    users = userGetAll()
    return {"users": users}
