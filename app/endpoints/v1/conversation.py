from fastapi import APIRouter, Header, Request, Form, File, UploadFile
from typing import Annotated, List, Union, Optional
from typing import Union
from pydantic import BaseModel
from app.model.user import userCreate, userLogin, userGet, userUpdate, userGetAll
from app.model.conversation import conversationCreate, conversationGet, verifyUserInConversation
from app.auth.verify import verify_token
from app.filestore.save import save_upload_file

router = APIRouter()


@router.post("/v1/conversation")
async def createConversation(
    name: str = Form(...),
    user_ids: list = Form(...),
    is_group: bool = Form(...),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    if not id in user_ids: user_ids.append(id)
    conversation = conversationCreate(name, user_ids, is_group)

    return {
        "detail": "ok",
        "conversation": conversation,
    }

@router.get("/v1/conversation")
async def getConversation(
    conversationId: int = Form(...),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    verifyUserInConversation(id, conversationId)
    conversation = conversationGet(conversationId)

    return {
        "detail": "ok",
        "conversation": conversation,
    }

