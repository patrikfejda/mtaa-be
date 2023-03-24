from fastapi import APIRouter, Request, Form, File, UploadFile
from app.model.user import userCreate, userLogin, userGet, userUpdate, userGetAll
from app.auth.verify import verifyToken
from app.handlefilestore.save import saveFilestore

router = APIRouter()


@router.post("/v1/user/register")
async def routerRegisterUser(
    email: str = Form(...), username: str = Form(...), password: str = Form(...)
):
    jwt, createdUser = userCreate(email=email, username=username, password=password)
    return {"accessToken": jwt, "user": createdUser}


@router.post("/v1/user/login")
async def routerLoginUser(username: str = Form(...), password: str = Form(...)):
    jwt, user = userLogin(username=username, password=password)
    return {"accessToken": jwt, "user": user}


@router.get("/v1/user")
async def routerGetUser(id: str = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    user = userGet(
        id=id,
    )
    return {"user": user}


@router.put("/v1/user")
async def routerUpdateUser(
    displayName: str = Form(None),
    profilePhoto: UploadFile = File(None),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    uploadedPhotoUrl = saveFilestore(profilePhoto)
    user = userUpdate(id, displayName, uploadedPhotoUrl)
    return {
        "detail": user["id"],
        "displayName": user["displayName"],
        "profilePhotoUrl": user["profilePhotoUrl"],
    }


@router.get("/v1/user/all")
async def routerGetAllUsers():
    users = userGetAll()
    return {"users": users}
