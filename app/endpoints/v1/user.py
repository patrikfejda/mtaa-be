from fastapi import APIRouter
from typing import Union
from pydantic import BaseModel
from app.model.user import userCreate, userLogin, userGet, userUpdate
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
    display_name: str or None
    profile_photo_url: str or None



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
async def updateUser(payload: UserObjectPut):
    payload = payload.dict()
    # TODO AUTH JWT
    userUpdate(payload["id"], payload["display_name"], payload["profile_photo_url"])
    return {"status": "ok"}
