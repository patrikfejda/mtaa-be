from fastapi import APIRouter
from typing import Union
from pydantic import BaseModel
from app.model.user import createUser, userLogin
router = APIRouter()


class UserObjectRegister(BaseModel):
    email: str
    username: str
    password: str

class UserObjectLogin(BaseModel):
    username: str
    password: str


@router.post("/v1/user/register")
async def registerUser(payload: UserObjectRegister):
    payload = payload.dict()

    jwt, createdUser = createUser(
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
