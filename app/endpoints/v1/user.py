from fastapi import APIRouter, Header, Request, Form
from typing import Annotated, List, Union
from typing import Union
from pydantic import BaseModel
from app.model.user import userCreate, userLogin, userGet, userUpdate, userGetAll
from app.auth.verify import verify_token
router = APIRouter()


@router.post("/v1/user/register")
async def registerUser(email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    jwt, createdUser = userCreate(
        email=email,
        username=username,
        password=password
    )
    return {"access_token": jwt, "user": createdUser}


@router.post("/v1/user/login")
async def loginUser(username: str = Form(...), password: str = Form(...)):
    jwt, user = userLogin(
        username=username,
        password=password
    )
    return {"access_token": jwt, "user": user}

@router.get("/v1/user")
async def getUser(id: str = Form(...)):
    user = userGet(
        id=id,
    )
    return {"user": user}

@router.put("/v1/user")
async def updateUser(id: str = Form(...), display_name: str = Form(...), profile_photo_url: str = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    verify_token(id, jwt)
    userUpdate(id, display_name, profile_photo_url)
    return {"detail": id, "display_name": display_name, "profile_photo_url": profile_photo_url}

@router.get("/v1/user/all")
def getAllUsers():
    users = userGetAll()
    return {"users": users}
