from fastapi import APIRouter, Header, Request, Form
from typing import Annotated, List, Union
from typing import Union
from pydantic import BaseModel
from app.model.user import userCreate, userLogin, userGet, userUpdate, userGetAll
from app.auth.verify import verify_token
router = APIRouter()


class UserObjectRegister(BaseModel):
    email: str
    username: str
    password: str

class UserObjectLogin(BaseModel):
    username: str
    password: str

class UserObjectId(BaseModel):
    id: int

class UserObjectPut(BaseModel):
    id: int
    display_name: str = None
    profile_photo_url: str = None



@router.post("/v1/user/register")
async def registerUser(payload: UserObjectRegister):
    payload = payload.dict()

    jwt, createdUser = userCreate(
        email=payload["email"],
        username=payload["username"],
        display_name=payload["username"],
        password=payload["password"],
    )

    return {"access_token": jwt, "user": createdUser}


@router.post("/v1/user/login")
async def loginUser(payload: UserObjectLogin):
    payload = payload.dict()
    jwt, user = userLogin(
        username=payload["username"],
        password=payload["password"],
    )

    return {"access_token": jwt, "user": user}

@router.get("/v1/user")
async def getUser(payload: UserObjectId):
    # TODO AUTH JWT
    payload = payload.dict()
    user = userGet(
        id=payload["id"],
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
